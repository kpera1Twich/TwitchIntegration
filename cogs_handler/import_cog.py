from core_cogs.brower_stuff import WebBrowserCommands
from core_cogs.jumpscares import JumpScareCommands
from core_cogs.minecraft import MinecraftCommands
from core_cogs.sound import AdjustAudioCommands
from core_cogs.wallpaper import WallpaperCommands
from twitchio.ext.commands import Bot, Cog


class ImportCogs(Cog):
    """A cog for the web browsing commands"""

    def __init__(self, bot: Bot):
        for cog in [
            WebBrowserCommands(bot),
            MinecraftCommands(bot),
            WallpaperCommands(bot),
            AdjustAudioCommands(bot),
            JumpScareCommands(bot),
        ]:
            bot.add_cog(cog)
