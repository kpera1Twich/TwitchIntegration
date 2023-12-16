"""Adds commands to jumpscare the streamer"""

import random
from pathlib import Path
from threading import Thread

from helper_functions.config_handler import enable_function_with_config
from helper_functions.validation import check_for_trusted_members
from playsound import PlaysoundException, playsound
from twitchio.ext.commands import Bot, Bucket, Cog, Context, command, cooldown


@enable_function_with_config(config="settings.sound.enabled")
class JumpScareCommands(Cog):
    """Cog for jumpscares"""

    def __init__(self, bot: Bot):
        super().__init__()
        self.__bot = bot

        self.__jumpscare_folder = Path("./resources/jumpscare stuff/sounds")
        self.__hello_sounds = []

        self.__recursively_iter_dir(
            self.__jumpscare_folder.joinpath("hello"), self.__hello_sounds
        )

        self.__enable_spamming = False

    @property
    def enable_spamming(self) -> bool:
        """Returns whether spamming scares is allowed

        :return: Whether spamming scares is allowed
        :rtype: bool
        """
        return self.__enable_spamming

    @command()
    async def enable_scare_spam(self, context: Context):
        """Enables scare spamming

        :param context:
        :type context:
        :return:
        :rtype:
        """
        if not await check_for_trusted_members(context.author.name):
            return

        self.__enable_spamming = True
        await context.reply("Scare Command Spamming Enabled")

    @command()
    async def disable_scare_spam(self, context: Context):
        """Disables scare spamming

        :param context:
        :type context:
        :return:
        :rtype:
        """

        if not await check_for_trusted_members(context.author.name):
            return

        self.__enable_spamming = False
        await context.reply("Scare Command Spamming Disabled")

    @enable_function_with_config(config="settings.sound.hello")
    async def hello_scare(self):
        """Plays a random "Hello" sound

        :return:
        :rtype:
        """
        playsound(str(random.choice(self.__hello_sounds)), False)

    def __recursively_iter_dir(self, file_path: Path, files: list[Path]):
        """Recursively iters a dir, add each file to a given list

        :param file_path: The path to start with
        :type file_path: Path
        :param files: The list to add to
        :type files: list[Path]
        :return:
        :rtype:
        """

        for path in file_path.iterdir():
            if not path.is_file():
                self.__recursively_iter_dir(path, files)
            else:
                files.append(path)
