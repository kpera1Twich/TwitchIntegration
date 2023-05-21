"""Commands to do with the windows wallpaper"""
from ctypes import Array, c_wchar, create_unicode_buffer, windll
from pathlib import Path
from random import choice

from helper_functions.validation import check_for_trusted_members
from twitchio.ext.commands import Bot, Bucket, Cog, Context, command, cooldown


class WallpaperCommands(Cog):
    """A cog for the web browsing commands"""

    def __init__(self, bot: Bot):
        super().__init__()
        self.__bot = bot

        self.__original_wallpaper = create_unicode_buffer(512)
        windll.user32.SystemParametersInfoW(
            0x73, len(self.__original_wallpaper), self.__original_wallpaper, 0
        )

    @cooldown(rate=1, per=1800, bucket=Bucket.channel)
    @command()
    async def set_random_wallpaper(self, context: Context):
        """Sets the windows background to a random image inside the resources/images file

        :param context:
        :type context:
        :return:
        :rtype:
        """
        if not await check_for_trusted_members(context.author.name):
            return
        directory = Path(".")
        while directory.is_dir():
            directory = choice([item for item in directory.iterdir()])

        file_path_bytes = create_unicode_buffer(512)
        file_path_bytes.value = str(directory.absolute())
        await self.__change_wallpaper(file_path_bytes)
        await context.reply(f"Wallpaper changed to {directory.name}")

    async def reset(self):
        """Resets the windows wallpaper to what it was

        :return:
        :rtype:
        """
        await self.__change_wallpaper(self.__original_wallpaper)

    @staticmethod
    async def __change_wallpaper(wallpaper_path: Array[c_wchar]):
        """Changes the windows wallpaper

        :param wallpaper_path: The path to the new wallpaper
        :type wallpaper_path: Array[c_wchar]
        :return:
        :rtype:
        """
        windll.user32.SystemParametersInfoW(0x14, 0, wallpaper_path, 0)
