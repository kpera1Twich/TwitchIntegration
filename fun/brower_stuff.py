"""Adds commands to do with the browser"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from twitchio.ext.commands import Bot, Cog, Context, command


class WebBrowserCommands(Cog):
    """A cog for the web browsing commands"""

    def __init__(self, bot: Bot):
        super().__init__()
        self.__bot = bot

    @command()
    async def rick_roll(self, ctx: Context):
        """Opens up "Never gonna give you up" in the background

        :param ctx:
        :type ctx:
        :return:
        :rtype:
        """
        firefox_options = webdriver.FirefoxOptions()
        firefox_options.add_argument("--disable-notifications")
        firefox_options.add_argument("--headless")
        driver = webdriver.Firefox(
            executable_path="geckodriver.exe",
            options=firefox_options,
        )
        driver.get("https://www.youtube.com/watch?v=dQw4w9WgXcQ")
        print("Rick-rolling!")
        # video_player = driver.find_element(By.ID, "movie_player")
        # video_player.send_keys(Keys.SPACE)
