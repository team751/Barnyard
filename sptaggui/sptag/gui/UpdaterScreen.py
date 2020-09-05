import os
import sys
import requests
import tempfile
import threading
import zipfile

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.progressbar import ProgressBar
from kivy.uix.screenmanager import Screen

from constants import CURRENT_MAX_VERSION, CURRENT_MIN_VERSION, CURRENT_PATCH_VERSION, GITHUB_API_LINK, \
    UPDATER_CONSIDER_PRE_RELEASES, UPDATER_GITHUB_REPO, UPDATER_KEY_PATH


class UpdaterScreen(Screen):
    _box_layout = None
    _summary_label = None
    _update_label = None
    _update_bar = None

    @staticmethod
    def version_greater(version_string: str, version_string_2: str):
        if version_string.startswith("v"):
            version_string = version_string.lstrip("v")
        if version_string_2.startswith("v"):
            version_string_2 = version_string_2.lstrip("v")

        version_nums = version_string.split(".")
        version_nums_2 = version_string_2.split(".")

        assert(len(version_nums) == 3 and len(version_nums_2) == 3)

        if version_nums[0] > version_nums_2[0]:
            return True
        elif version_nums[0] == version_nums_2[0]:
            if version_nums[1] > version_nums_2[1]:
                return True
            elif version_nums[1] == version_nums_2[1]:
                return version_nums[2] > version_nums_2[2]
            else:
                return False
        else:
            return False

    @staticmethod
    def get_update():
        headers = {}

        if UPDATER_KEY_PATH != "":
            with open(UPDATER_KEY_PATH, 'r') as token_file:
                headers["Authorization"] = "token " + token_file.read().strip("\n")

        try:
            releases_request = requests.get(GITHUB_API_LINK + "/repos/" + UPDATER_GITHUB_REPO + "/releases",
                                            headers=headers)
        except requests.exceptions.ConnectionError:
            return None

        releases_request.raise_for_status()

        our_version = "v" + str(CURRENT_MAX_VERSION) + "." + str(CURRENT_MIN_VERSION) + "." + str(CURRENT_PATCH_VERSION)
        releases_json = releases_request.json()

        greatest_release_dict = None
        greatest_version = our_version

        for release in releases_json:
            if not release["prerelease"] or UPDATER_CONSIDER_PRE_RELEASES:
                if UpdaterScreen.version_greater(release["tag_name"], greatest_version):
                    greatest_release_dict = release
                    greatest_version = release["tag_name"]

        if greatest_version != our_version:
            assert(greatest_release_dict is not None)

            return greatest_release_dict
        else:
            return None

    def _download_update(self, release_dict: dict):
        headers = {
            "Accept": "application/octet-stream"
        }

        if UPDATER_KEY_PATH != "":
            with open(UPDATER_KEY_PATH, 'r') as updater_key_file:
                headers["Authorization"] = "token " + updater_key_file.read().strip("\n")

        response = requests.get(release_dict["assets"][0]["url"], headers=headers, stream=True)

        print(str(headers))

        response.raise_for_status()

        total = int(release_dict["assets"][0]["size"])

        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            zip_file_path = temp_file.name

            if total is None:
                temp_file.write(response.content)

                self._update_bar = 100
            else:
                downloaded = 0

                for data in response.iter_content(chunk_size=40960):
                    downloaded += len(data)
                    temp_file.write(data)

                    self._update_bar.value = downloaded / total

        with zipfile.ZipFile(zip_file_path, 'r') as zip_file:
            script_path = os.path.dirname(os.path.realpath(sys.modules['__main__'].__file__))

            print("Extracting to " + script_path)

            zip_file.extractall(script_path)

        os.remove(zip_file_path)

        args = sys.argv[:]

        args.insert(0, sys.executable)
        if sys.platform == 'win32':
            args = ['"%s"' % arg for arg in args]

        os.execv(sys.executable, args)

    def __init__(self):
        super().__init__(name="Updater Screen")

        self._box_layout = BoxLayout(orientation='vertical', spacing=10)

        self.add_widget(self._box_layout)

    def start_update(self, update_dict: dict):
        if update_dict is None:
            self._current_update = UpdaterScreen.get_update()
        else:
            self._current_update = update_dict

        if self._current_update is not None:
            self._update_label = Label(text="Downloading update " + self._current_update["tag_name"])
            self._update_bar = ProgressBar(max=100)

            self._box_layout.add_widget(self._update_label)
            self._box_layout.add_widget(self._update_bar)

            thread = threading.Thread(target=self._download_update, args=(self._current_update,))

            thread.start()
