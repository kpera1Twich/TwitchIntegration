from twitchio.ext.commands import Bot, Cog, Context, command

from .brower_stuff import WebBrowserCommands


class ImportCogs(Cog):
    """A cog for the web browsing commands"""

    def __init__(self, bot: Bot):
        for cog in [
            WebBrowserCommands(bot),
        ]:
            bot.add_cog(cog)
