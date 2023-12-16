"""Commands for if the person is playing minecraft"""
from helper_functions.config_handler import enable_function_with_config
from helper_functions.enums import Keys
from helper_functions.key_commands import hold_key, press_key, release_key
from twitchio.ext.commands import Bot, Bucket, Cog, Context, command, cooldown


@enable_function_with_config(config="settings.minecraft.enabled")
class MinecraftCommands(Cog):
    """A cog for the web browsing commands"""

    def __init__(self, bot: Bot):
        super().__init__()
        self.__bot = bot

    @enable_function_with_config(config="settings.minecraft.throw item")
    @cooldown(rate=1, per=600, bucket=Bucket.member)
    @cooldown(rate=5, per=300, bucket=Bucket.subscriber)
    @command()
    async def throw_item(self, ctx: Context):
        """Throws a singular item out of the hand/what the mouse is currently hovering over

        :param ctx:
        :type ctx:
        :return:
        :rtype:
        """

        await press_key(Keys.Q)  # Default key is Q

    @enable_function_with_config(config="settings.minecraft.throw stack")
    @cooldown(rate=1, per=600, bucket=Bucket.member)
    @cooldown(rate=5, per=300, bucket=Bucket.subscriber)
    @command()
    async def throw_stack(self, ctx: Context):
        """Throws a whole stack out of the hand/what the mouse is currently hovering over

        :param ctx:
        :type ctx:
        :return:
        :rtype:
        """

        await hold_key(Keys.LEFT_CONTROL)
        await press_key(Keys.Q)  # Default key is Q
        await release_key(Keys.LEFT_CONTROL)

    async def reset(self):
        """Resets everything done by this cog

        :return:
        :rtype:
        """
