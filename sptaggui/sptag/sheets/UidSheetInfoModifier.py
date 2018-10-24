import gspread

from os import getcwd

from oauth2client.service_account import ServiceAccountCredentials

SCOPES = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']
SPREADSHEET_KEY = "1zRSYqFLEEHLTDiMwv_tjmZ2aUK3V4LZ9E4OVBDFX_OI"


class UidSheetInfoModifier:
    _sheets_service = None
    _current_sheet = None

    class PartInfo(object):
        uid = None
        name = None
        description = None
        location = None
        image_url = None

        def __init__(self, uid=None, name=None, description=None, location=None,
                     image_url=None):
            self.uid = uid
            self.name = name
            self.description = description
            self.location = location
            self.image_url = image_url

    def __init__(self):
        credentials = ServiceAccountCredentials.\
            from_json_keyfile_name("client_secret.json", SCOPES)

        self._sheets_service = gspread.authorize(credentials)
        self._current_sheet = self._sheets_service.open_by_key(SPREADSHEET_KEY).sheet1

    def _uid_to_row_number(self, uid):
        uidsFound = self._current_sheet.col_values(1)

        if uidsFound:
            for i in range(len(uidsFound)):
                if uid == int(uidsFound[i]):
                    return i

        # No UIDs representing this UID found in this table.
        return None

    def get_part_info(self, uid):
        rowNumToUse = self._uid_to_row_number(uid)

        if not rowNumToUse:
            return None

        partInfoArray = self._current_sheet.row_values(rowNumToUse)

        if len(partInfoArray) >= 5:
            return UidSheetInfoModifier.PartInfo(partInfoArray[0],
                                            partInfoArray[1], partInfoArray[2],
                                            partInfoArray[3], partInfoArray[4])
        else:
            return None