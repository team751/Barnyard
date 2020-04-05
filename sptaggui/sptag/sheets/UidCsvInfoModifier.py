import csv
import datetime

from pathlib import Path

from sptag.sheets.PartInfo import PartInfo
from sptag.sheets.PartSheetModifierInterface import PartSheetModifierInterface


class UidCsvInfoModifier(PartSheetModifierInterface):
    def _get_csv_rows(self):
        rows = []
    
        with open(str(Path.home()) + "/Barnyard-2/offlinesheet.csv", 
                  "r") as csv_file:
            for row in csv.reader(csv_file, delimiter=','):
                rows.append(row)
        
        return rows

    def _update_edit_time(self, needs_sync=True):
        rows = self._get_csv_rows()
    
        with open(str(Path.home()) + "/Barnyard-2/offlinesheet.csv", 
                  "w") as csv_file:
            sheet_writer = csv.writer(csv_file)
            
            for row in rows:
                if row[0] == "Time Last Updated":
                    if needs_sync:
                        sheet_writer.writerow(["Time Last Updated", 
                                               datetime.datetime(2000, 1, 1).\
                                               now().ctime(), "needs_sync"])
                    else:
                        sheet_writer.writerow(["Time Last Updated", 
                                               datetime.datetime(2000, 1, 1).\
                                               now().ctime()])
                else:
                    sheet_writer.writerow(row)

    def add_part(self, part_info):
        self._update_edit_time()
    
        with open(str(Path.home()) + "/Barnyard-2/offlinesheet.csv", 
                  "a") as csv_file:
            sheet_writer = csv.writer(csv_file)
        
            sheet_writer.writerow([part_info.uid, part_info.name, 
                                   part_info.description, part_info.location, 
                                   part_info.image_url])

    def close(self):
        self._csv_file.close()
    
    def delete_part(self, part_info):
        self._update_edit_time()        
        rows = self._get_csv_rows()
    
        with open(str(Path.home()) + "/Barnyard-2/offlinesheet.csv", 
                  "w") as csv_file:
            sheet_writer = csv.writer(csv_file)
            
            for row in rows:
                if row[0] != part_info.uid:
                    sheet_writer.writerow(row)

    def edit_part(self, part_info):
        self._update_edit_time()
        rows = self._get_csv_rows()
    
        with open(str(Path.home()) + "/Barnyard-2/offlinesheet.csv", 
                  "w") as csv_file:
            sheet_writer = csv.writer(csv_file)
            
            print("editing")
            for row in rows:
                print(row[0] + "=====" + part_info.uid)
                if row[0] == part_info.uid:
                    sheet_writer.writerow([part_info.uid, part_info.name, 
                                           part_info.description, part_info.location, 
                                           part_info.image_url])
                    print("Edit written")
                else:
                    sheet_writer.writerow(row)
            

    def get_part_info(self, uid):
        for row in self._get_csv_rows():
            if row[0] == uid and len(row) >= 5:
                return PartInfo(row[0], row[1], row[2], row[3], row[4])
        
        return None

    def get_last_update(self):
        for row in self._get_csv_rows():
            if row[0] == "Time Last Updated":
                return row[1]
        
        return ""

    def search_for_parts(self, name=None, description=None, location=None):
        return_value = []

        for row in self._get_csv_rows():
            found = True

            if name is not None:
                found = row[1].startswith(name)

            if description is not None:
                found = row[2].startswith(name)

            if location is not None:
                found = row[3].startswith(name)

            if found:
                return_value.append(PartInfo(row[0], row[1], row[2], row[3],
                                             row[4]))

        return return_value
