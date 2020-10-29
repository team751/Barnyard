import _thread
import csv
import datetime
import os
import requests
import urllib3
import urllib.request
import urllib.parse

import gspread

from pathlib import Path
from threading import Lock

from oauth2client.service_account import ServiceAccountCredentials

from constants import GOOGLE_AUTH_JSON_PATH, GOOGLE_SPREADSHEET_KEY

from sptag.sheets.PartInfo import PartInfo
from sptag.sheets.PartSheetModifierInterface import PartSheetModifierInterface
from sptag.sheets.UidCsvInfoModifier import UidCsvInfoModifier

SCOPES = ['https://spreadsheets.google.com/feeds',
          'https://www.googleapis.com/auth/drive']


class UidSheetInfoModifier(PartSheetModifierInterface):
    _current_sheet = None
    _download_lock = None
    _sheets_service = None

    @staticmethod
    def is_url(url):
        try:
            result = urllib.parse.urlparse(url)
            return all([result.scheme, result.netloc, result.path])
        except:
            return False

    def __init__(self, download_lock: Lock = None):
        credentials = ServiceAccountCredentials. \
            from_json_keyfile_name(GOOGLE_AUTH_JSON_PATH, SCOPES)

        self._sheets_service = gspread.authorize(credentials)

        self._current_sheet = self._sheets_service.open_by_key(GOOGLE_SPREADSHEET_KEY).sheet1
        self._download_lock = download_lock

        Path(str(Path.home()) + "/Barnyard-2/").mkdir(exist_ok=True)

        try:
            with open(str(Path.home()) + "/Barnyard-2/offlinesheet.csv",
                      "r") as csv_file:
                for row in csv.reader(csv_file):
                    if row[0] == "Time Last Updated":
                        if len(row) > 2 and row[2] == "needs_sync":
                            print("syncing sheet")
                            self.sync_offline_sheet(True)

                            UidCsvInfoModifier()._update_edit_time(False)

        except OSError:
            pass  # Fine if csv file isn't found yet

        _thread.start_new_thread(self.make_data_offline, ())
        _thread.start_new_thread(self.make_images_offline, ())

    def _uid_to_row_number(self, uid):
        uidsFound = self._current_sheet.col_values(1)

        if uidsFound:
            for i in range(len(uidsFound)):
                if uidsFound[i].isdigit() and uid == uidsFound[i]:
                    print("uid found " + str(uidsFound[i]) + "=" + str(uid) + " (" + str(i) + ")")
                    return i

        # No UIDs representing this UID found in this table.
        return None

    def add_part(self, part_info):
        row_num = str(len(self._current_sheet.col_values(1)) + 1)

        print("Adding part...")

        self._current_sheet.update("A" + row_num + ":E" + row_num,
                                   [[part_info.uid, part_info.name, part_info.description,
                                    part_info.location, part_info.image_url]])

    def delete_part(self, part_info):
        row_num = self._uid_to_row_number(part_info.uid) + 1

        if row_num is not None:
            self._current_sheet.delete_row(row_num)

    def edit_part(self, part_info):
        row_num = str(self._uid_to_row_number(part_info.uid) + 1)

        if row_num is None:
            self.add_part(part_info)

        print("Editing part...")

        self._current_sheet.update("A" + row_num + ":E" + row_num,
                                   [[part_info.uid, part_info.name, part_info.description,
                                     part_info.location, part_info.image_url]])

    def get_part_info(self, uid):
        rowNumToUse = self._uid_to_row_number(uid)

        if rowNumToUse is None:
            return None

        partInfoArray = self._current_sheet.row_values(rowNumToUse + 1)

        if len(partInfoArray) >= 5:
            return PartInfo(partInfoArray[0], partInfoArray[1],
                            partInfoArray[2], partInfoArray[3],
                            partInfoArray[4])
        else:
            return None

    def make_data_offline(self):
        with open(str(Path.home()) + "/Barnyard-2/offlinesheet.csv", "w") as csv_file:
            offline_csv = csv.writer(csv_file)
            sheet_data = self._current_sheet.get_all_values()

            offline_csv.writerow(["Time Last Updated", datetime.datetime(2000, 1, 1).now().ctime()])

            for row in sheet_data:
                offline_csv.writerow(row)

    def make_images_offline(self):
        for row in self._current_sheet.get_all_values():
            if self.is_url(row[4]):
                # disabling urllib3 dh key error on RPI 3
                # https://stackoverflow.com/a/41041028

                if self._download_lock is not None:
                    self._download_lock.acquire()

                requests.packages.urllib3.disable_warnings()
                requests.packages.urllib3.util.ssl_.DEFAULT_CIPHERS += 'HIGH:!DH:!aNULL'
                try:
                    requests.packages.urllib3.contrib.pyopenssl.DEFAULT_SSL_CIPHER_LIST += 'HIGH:!DH:!aNULL'
                except AttributeError:
                    # no pyopenssl support used / needed / available
                    pass

                image_page = requests.get(row[4], verify=False)

                with open(str(Path.home()) + "/Barnyard-2/downloaded_" + row[0] +
                          os.path.splitext(row[4])[-1], 'wb') as image_file:
                    image_file.write(image_page.content)

                if self._download_lock is not None:
                    self._download_lock.release()
            # urllib.request.urlretrieve(row[4], )

    def search_for_parts(self, name=None, description=None, location=None):
        return_value = []

        for row in self._current_sheet.get_all_values():
            if row[0] is None or row[1] is None or row[2] is None or \
                    row[3] is None or row[4] is None or row[0] == "UID":
                continue

            found = True

            if name is not None:
                found = row[1].lower().startswith(name.lower())

            if description is not None:
                found = row[2].lower().startswith(description.lower())

            if location is not None:
                found = row[3].lower().startswith(location.lower())

            if found:
                return_value.append(PartInfo(row[0], row[1], row[2], row[3],
                                             row[4]))

        return return_value

    def sync_offline_sheet(self, overwrite=False):
        with open(str(Path.home()) + "/Barnyard-2/offlinesheet.csv", "r") as csv_file:
            offline_csv = csv.reader(csv_file)

            if overwrite:
                ranges = []
                rows = []

                for i in range(len(self._current_sheet.get_all_values())):
                    self._current_sheet.delete_row(i + 1)

                for row in offline_csv:
                    rows.append(row)

                for r in range(len(rows)):
                    if rows[r][0] != "Time Last Updated":
                        current_range = {
                            "range": "A" + str(r + 1) + chr(len(rows[r]) + 65),
                            "values": [[]]
                        }

                        for c in range(len(rows[r])):
                            current_range["values"][0].append(rows[r][c])

                        ranges.append(current_range)
            else:
                parts = []
                ranges = []
                sheet_values = self._current_sheet.get_all_values()

                for part in offline_csv:
                    parts.append(part)

                for i in range(len(sheet_values)):
                    for i2 in range(len(parts)):
                        if part[i2][0] == sheet_values[i][0]:
                            ranges.append({
                                "range": "B" + str(i) + ":E" + str(i),
                                "values": [[part[i2][1], part[i2][2], part[i2][3], part[i2][4]]]
                            })

                self._current_sheet.batch_update(ranges)
