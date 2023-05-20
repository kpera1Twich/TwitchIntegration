"""Commands for sounds"""

from ctypes import POINTER, c_float, cast, windll
from subprocess import PIPE, CompletedProcess, run

from helper_functions.validation import check_for_users
from twitchio.ext.commands import Bot, Cog, Context, command


class AdjustAudioCommands(Cog):
    """A cog for adjusting audio"""

    def __init__(self, bot: Bot):
        super().__init__()
        self.__bot = bot

        self.__audio_sources = []
        self.__default_mic_settings = {}
        self.__default_speaker_settings = {}
        self.__original_sound_level: c_float = c_float(0)

        self.__get_audio_sources()
        self.__get_default_settings()

    async def mute_mic(self):
        """Mutes the mic

        :return:
        :rtype:
        """
        self.__run_powershell_command("RecordingMute True")

    async def reset(self):
        """Resets all the audio

        :return:
        :rtype:
        """

        for device in self.__audio_sources:
            if device["Default"] == "True":
                self.__run_powershell_command(
                    f"Set-AudioDevice -ID {device['ID']} -DefaultOnly"
                )
        self.__run_powershell_command(
            f"RecordingMute {self.__default_mic_settings['muted']}"
        )
        self.__run_powershell_command(
            f"PlaybackMute {self.__default_speaker_settings['muted']}"
        )
        self.__run_powershell_command(
            f"RecordingVolume {self.__default_mic_settings['volume']}"
        )
        self.__run_powershell_command(
            f"PlaybackVolume {self.__default_speaker_settings['volume']}"
        )

    def __get_audio_sources(self):
        """Gets all the audio sources on the device

        :return:
        :rtype:
        """
        output = self.__run_powershell_command("get-audiodevice -list")
        devices = output.stdout.decode("utf-8").split("\r\n\r\n")

        for item in devices:
            if item.strip() == "":
                continue
            index, default, _, device_type, _, device_id, device = item.split("\r\n")
            self.__audio_sources.append(
                {
                    "Index": index.split(":").strip(),
                    "Default": default.split(":").strip(),
                    "Type": device_type.split(":").strip(),
                    "ID": device_id.split(":").strip(),
                    "Device": device.split(":").strip(),
                }
            )

    def __get_default_settings(self):
        """Gets the default settings for the audio sources

        :return:
        :rtype:
        """
        mic_muted = self.__run_powershell_command("Get-AudioDevice -RecordingMute")
        mic_volume = self.__run_powershell_command("Get-AudioDevice -RecordingVolume")
        speaker_muted = self.__run_powershell_command("Get-AudioDevice -PlaybackMute")
        speaker_volume = self.__run_powershell_command(
            "Get-AudioDevice -PlaybackVolume"
        )

        self.__default_mic_settings = {
            "muted": mic_muted.stdout.decode("utf-8"),
            "volume": mic_volume.stdout.decode("utf-8").split("%")[0],
        }
        self.__default_speaker_settings = {
            "muted": speaker_muted.stdout.decode("utf-8"),
            "volume": speaker_volume.stdout.decode("utf-8").split("%")[0],
        }

    @staticmethod
    def __run_powershell_command(command_to_run: str) -> CompletedProcess:
        """Runs a command on the powershell

        :param command_to_run: The command to run
        :type command_to_run: str
        :return: The output of the command
        :rtype: CompletedProcess
        """
        return run(["powershell", "-Command", command_to_run], stdout=PIPE)
