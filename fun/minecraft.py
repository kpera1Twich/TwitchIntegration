"""Commands for if the person is playing minecraft"""

from helper_functions.enums import Keys
from helper_functions.key_commands import hold_key, press_key, release_key
from helper_functions.validation import check_for_user
from twitchio.ext.commands import Bot, Cog, Context, command


class MinecraftCommands(Cog):
    """A cog for the web browsing commands"""

    def __init__(self, bot: Bot):
        super().__init__()
        self.__bot = bot

    @command()
    async def throw_item(self, ctx: Context):
        """Throws a singular item out of the hand/what the mouse is currently hovering over

        :param ctx:
        :type ctx:
        :return:
        :rtype:
        """
        if not await check_for_user(ctx.author.name):
            await ctx.reply("You cannot do this command!")

        await press_key(Keys.Q)  # Default key is Q

    @command()
    async def throw_stack(self, ctx: Context):
        """Throws a whole stack out of the hand/what the mouse is currently hovering over

        :param ctx:
        :type ctx:
        :return:
        :rtype:
        """
        if not await check_for_user(ctx.author.name):
            await ctx.reply("You cannot do this command!")

        await hold_key(Keys.LEFT_CONTROL)
        await press_key(Keys.Q)  # Default key is Q
        await release_key(Keys.LEFT_CONTROL)
