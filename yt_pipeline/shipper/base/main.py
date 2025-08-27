from dataclasses import asdict
import os

from yt_pipeline.utils import get_current_time, dict_to_json
from yt_pipeline.container.base import BaseItem


class BaseShipper:
    def __init__(self):
        self.main_records: list[dict] = list()
        self.thumbnails: dict[str, list] = dict()
        self.output_folder = "backup/BaseShipper"
            
    def invoke(self, items: list[BaseItem], output_folder=None, backup=True) -> None:
        """
        run the shipper and save flattened records to class attributes
        """
        for item in items:
            self._extract_details(item)

        if backup:
            self._handle_backup(self.main_records, suffix=" main records", output_folder=output_folder)
            self._handle_backup(self.thumbnails, suffix=" thumbnails", output_folder=output_folder)
    
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