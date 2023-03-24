from twitchio.ext.commands import Bot, Cog, Context, command

from .brower_stuff import WebBrowserCommands
from .minecraft import MinecraftCommands
from .wallpaper import WallpaperCommands


class ImportCogs(Cog):
    """A cog for the web browsing commands"""

    def __init__(self, bot: Bot):
        for cog in [
            WebBrowserCommands(bot),
            MinecraftCommands(bot),
            WallpaperCommands(bot),
        ]:
            bot.add_cog(cog)
