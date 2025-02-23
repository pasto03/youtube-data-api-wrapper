from dataclasses import asdict
import os

from youtube_data_api.utils import get_current_time, dict_to_json
from youtube_data_api.container.base import BaseItem


class BaseShipper:
    def __init__(self):
        self.main_records: list[dict] = list()
        self.thumbnails: list[dict] = list()
        self.output_folder = "backup/BaseShipper"
            
    def invoke(self, items: list[BaseItem], output_folder=None, backup=True) -> None:
        """
        run the shipper and obtain output
        """
        
        for item in items:
            self.main_records.append(self._extract_details(item))
            self.thumbnails.extend(self._extract_thumbnails(item))
        
        if backup:
            self._handle_backup(self.main_records, suffix=" main records", output_folder=output_folder)
            self._handle_backup(self.thumbnails, suffix=" thumbnails", output_folder=output_folder)
        
        print("All records have been packed.")
#         return self.main_records, self.thumbnails
    
    def _handle_backup(self, records: list[dict], suffix="", output_folder=None):
        output_folder = self.output_folder if not output_folder else output_folder
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)
        filename = get_current_time() + suffix + ".json"
        records = dict_to_json(records)
        with open(os.path.join(output_folder, filename), "wb") as f:
            f.write(records.encode("utf-8"))
    
    @staticmethod
    def _extract_details(item: BaseItem) -> dict:
        raise NotImplementedError
    
    @staticmethod
    def _extract_thumbnails(item: BaseItem) -> list[dict]:
        """
        return a list of dict of thumbnails
        """
        raise NotImplementedError