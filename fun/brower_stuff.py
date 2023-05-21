"""Adds commands to do with the browser"""
from asyncio import sleep

from helper_functions.validation import check_for_trusted_members
from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.webdriver import WebDriver
from twitchio.ext.commands import Bot, Bucket, Cog, Context, command, cooldown


class WebBrowserCommands(Cog):
    """A cog for the web browsing commands"""

    def __init__(self, bot: Bot):
        super().__init__()
        self.__bot = bot
        self.__windows: list[WebDriver] = []

    @cooldown(rate=0, per=600, bucket=Bucket.member)
    @cooldown(rate=1, per=600, bucket=Bucket.subscriber)
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
        self.__windows.append(driver)

        driver.get("https://www.youtube.com/watch?v=dQw4w9WgXcQ")

        # Make sure the page is loaded
        await sleep(5)

        # Press the "Reject Cookies" button if the cookie policy appears
        try:
            reject_cookies = driver.find_element(
                By.XPATH,
                "/html/body/ytd-app/ytd-consent-bump-v2-lightbox/tp-yt-paper-dialog/div[4]/div[2]/div[6]/div["
                "1]/ytd-button-renderer[1]/yt-button-shape/button",
            )
            reject_cookies.click()
        except NoSuchElementException:
            ...

        # Play the video
        video = driver.find_element(By.ID, "movie_player")
        video.send_keys(Keys.SPACE)  # hits space

        # Check to see if there is an add
        try:
            driver.find_element(
                By.XPATH,
                "/html/body/ytd-app/div[1]/ytd-page-manager/ytd-watch-flexy/div[5]/div[1]/div/div[1]/div["
                "2]/div/div/ytd-player/div/div/div[4]/div/div[2]",
            )
            await self.__handle_youtube_ads(driver)
        except NoSuchElementException:
            ...

        print("Rick-rolling!")
        await sleep(3 * 60 + 33)  # Sleep for the duration of the song

        driver.close()  # Make sure the window closes
        self.__windows.remove(driver)

    async def reset(self):
        """Resets everything which has happened

        :return:
        :rtype:
        """
        for window in self.__windows:
            window.close()

    @staticmethod
    async def __handle_youtube_ads(driver: WebDriver):
        """Handles the Youtube ads

        :param driver:
        :type driver:
        :return:
        :rtype:
        """
        # Wait a fraction of a second to allow the ad to load
        await sleep(0.2)
        mute_button = driver.find_element(
            By.XPATH,
            "/html/body/ytd-app/div[1]/ytd-page-manager/ytd-watch-flexy/div[5]/div[1]/div/div[1]/div["
            "2]/div/div/ytd-player/div/div/div[26]/div[2]/div[1]/span/button",
        )
        # Mute the ad.
        # We don't know if the ad is already muted, so just press the down button 20 times to avoid accidentally
        # enabling sound again
        for _ in range(20):
            mute_button.send_keys(Keys.ARROW_DOWN)

        try:
            unskippable_ad = driver.find_element(By.XPATH, '// * [ @ id = "ad-text:g"]')
            # The ad cannot be skipped, wait for it to be done
            print(unskippable_ad.text)
            await sleep(
                int(unskippable_ad.text.split("Your video will being in ")[1].strip())
            )
            for _ in range(20):
                mute_button.send_keys(Keys.ARROW_UP)

            # Seeing as there may be multiple unskippable ads, return to this function
            await WebBrowserCommands.__handle_youtube_ads(driver)
        except NoSuchElementException:
            try:
                skippable_ad = driver.find_element(By.XPATH, '//*[@id="ad-text:3"]')
                # The ad can be skipped. Wait however long is needed and then press the skip ad button
                await sleep(int(skippable_ad.text.strip()) + 1)
                skip_ad_button = driver.find_element(By.XPATH, '//*[@id="ad-text:6"]')

                # Pause the video so we don't play any part of the ad
                video = driver.find_element(By.ID, "movie_player")
                video.send_keys(Keys.SPACE)  # hits space

                for _ in range(20):
                    mute_button.send_keys(Keys.ARROW_UP)
                skip_ad_button.click()
            except NoSuchElementException:
                print("What happened?")
                ...
