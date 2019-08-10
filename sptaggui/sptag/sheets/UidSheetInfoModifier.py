import gspread

from os import getcwd

from oauth2client.service_account import ServiceAccountCredentials

SCOPES = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']
SPREADSHEET_KEY = "1zRSYqFLEEHLTDiMwv_tjmZ2aUK3V4LZ9E4OVBDFX_OI"

class PartInfo(object):
    uid = None
    name = None
    description = None
    location = None
    image_url = None

    def __init__(self, uid=None, name=None, description=None, 
                 location=None, image_url=None):
        self.uid = uid
        self.name = name
        self.description = description
        self.location = location
        self.image_url = image_url

class UidSheetInfoModifier:
    _sheets_service = None
    _current_sheet = None

    def __init__(self):
        credentials = ServiceAccountCredentials.\
            from_json_keyfile_name("client_secret.json", SCOPES)

        self._sheets_service = gspread.authorize(credentials)
        self._current_sheet = self._sheets_service.open_by_key(SPREADSHEET_KEY).sheet1

    def _uid_to_row_number(self, uid):
        uidsFound = self._current_sheet.col_values(1)

        if uidsFound:
            for i in range(len(uidsFound)):
                if uidsFound[i].isdigit() and uid == uidsFound[i]:
                    print("uid found " + str(uidsFound[i]) + "=" + str(uid) + " (" + str(i) + ")")
                    return i

        # No UIDs representing this UID found in this table.
        return None

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
    
    def add_part(self, part_info):
        uidsFound = len(self._current_sheet.col_values(1))
        
        self._current_sheet.update_cell(uidsFound + 1, 1,
                                        part_info.uid)
        self._current_sheet.update_cell(uidsFound + 1, 2,
                                        part_info.name)
        self._current_sheet.update_cell(uidsFound + 1, 3,
                                        part_info.description)
        self._current_sheet.update_cell(uidsFound + 1, 4,
                                        part_info.location)
        self._current_sheet.update_cell(uidsFound + 1, 5,
                                        part_info.image_url)
