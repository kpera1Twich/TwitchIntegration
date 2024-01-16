#! ./venv/Scripts/python
"""A program which can respond to messages sent in twitch chat.

The bot should be able to connect to GITHUB so that it can check to see if any commands have changed, and if so,
download them and re-import the commands
"""
from asyncio import create_subprocess_shell, get_running_loop, sleep
from asyncio.subprocess import PIPE
from importlib import reload
from os import getcwd, getenv
from sys import modules

from dotenv import load_dotenv
from twitchio import Message
from twitchio.ext.commands import Bot, Cog, Context, command

from cogs_handler.import_cog import ImportCogs
from helper_functions.config_handler import enable_function_with_config
from helper_functions.enums import ScreenRotation
from helper_functions.key_commands import hold_and_release_key
from helper_functions.validation import check_for_trusted_members

load_dotenv(".env", override=True)
load_dotenv("DO NOT OPEN ON CAM/.env.account_details", override=True)


class StreamIntegrationsBot(Bot):
    def __init__(self):
        super().__init__(
            token=getenv("ACCESS_TOKEN"),
            prefix="-",
            initial_channels=getenv("CHANNELS").split(","),
        )

        self.__hello_peeps = []

    async def event_ready(self):
        """Does some bits when the bot has connected to twitch

        :return:
        :rtype:
        """
        print(f"We have connected as {self.nick}")
        self.add_cog(ImportCogs(bot))
        print("Added Cogs")

    async def add_cogs(self, cogs: list[Cog]):
        """Adds all the cogs to the bot

        :param cogs: The cogs to add to the bot
        :type cogs: list[Cog]
        :return:
        :rtype:
        """
        for cog in cogs:
            self.add_cog(cog)

    # noinspection PyUnresolvedReferences
    async def event_message(self, message: Message):
        """Handles messages in case there is an event that needs to be done

        :param message: The message that was sent
        :type message: Message
        :return:
        :rtype:
        """
        if message.echo:
            return  # Don't handle messages sent by the bot

        if any(
            [
                message.content.lower() == "hello",
                message.content.lower() == "hi",
                message.content.lower() == "hey",
                message.content.lower() == "07",
            ]
        ) and ("JumpScareCommands" in self.cogs.keys()):
            jump_scare_commands = self.cogs.get("JumpScareCommands")
            if (
                message.author in self.__hello_peeps
                and not jump_scare_commands.enable_spamming
            ):
                return
            elif message.author not in self.__hello_peeps:
                self.__hello_peeps.append(message.author)

            await self.cogs.get("JumpScareCommands").hello_scare()

        else:
            await self.handle_commands(message)

    @command()
    async def ping(self, ctx: Context):
        """Sends a simple reply of "pong" back to the user

        :param ctx:
        :type ctx:
        :return:
        :rtype:
        """

        await ctx.reply("pong!")

    @command()
    async def test(self, ctx: Context):
        """Test method

        :param ctx:
        :type ctx:
        :return:
        :rtype:
        """
        if ctx.author.name == "kpera1":
            await ctx.send("test")

    @enable_function_with_config(config="settings.ungrouped.flip screen")
    @command()
    async def flip_screen(self, ctx: Context):
        """Flips the orientation of the screen

        :param ctx:
        :type ctx:
        :return:
        :rtype:
        """
        if not await check_for_trusted_members(ctx.author.name):
            await ctx.reply("You cannot do this command!")
            return
        args = ctx.message.content.split("-flip_screen")
        if len(args) > 0:
            match args[1].strip():
                case "up":
                    rotation = ScreenRotation.UP
                case "down":
                    rotation = ScreenRotation.DOWN
                case "left":
                    rotation = ScreenRotation.LEFT
                case "right":
                    rotation = ScreenRotation.RIGHT
                case _:
                    await ctx.reply(f"Unknown argument {args[1]}")
                    return

            for button in rotation:
                await hold_and_release_key(button, 1)

    @command()
    async def check_for_updated_cogs(self, ctx: Context):
        """Manually checks for updated cogs

        :param ctx:
        :type ctx:
        :return:
        :rtype:
        """
        if not await check_for_trusted_members(ctx.author.name):
            await ctx.reply("You cannot do this command!")
            return
        print("Checking")
        await self.__check_for_updated_cogs()
        await ctx.reply("Reloaded cogs!")

    async def __check_for_updated_cogs(self) -> bool:
        """Checks the github repo to see if there are any updated cogs

        :return: Whether the cogs have been updated
        :rtype: bool
        """
        shell = await create_subprocess_shell(
            """git fetch --all & git checkout -B "main" "origin/main" -f""",
            stdout=PIPE,
            stderr=PIPE,
        )
        stdout, stderr = await shell.communicate()
        print(f"{stdout.decode()=}; {len(stdout.decode())=}")
        print(f"{stderr.decode()=}; {len(stderr.decode())=}")

        if stderr.decode().startswith("Reset branch"):
            await self.__reload_cogs()
            return True

    async def __reload_cogs(self):
        """Unloads then reloads all the cogs

        :return:
        :rtype:
        """
        cogs = {k: v for k, v in self.cogs.items()}
        for cog in cogs:
            await cog.reset()
            self.remove_cog(cog)

        reload_module = modules["fun"]
        reload(reload_module)
        self.add_cog(ImportCogs(self))
        for cog in self.cogs:
            print(cog.title())


bot = StreamIntegrationsBot()

try:
    bot.run()
except Exception as e:
    print(e)
    cogs = {k: v for k, v in bot.cogs.items()}
    loop = get_running_loop()
    for cog in cogs:
        loop.run_until_complete(cog.reset())
