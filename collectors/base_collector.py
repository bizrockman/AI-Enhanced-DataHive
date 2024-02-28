from collections.abc import Collection

from models import Media

from dao.dao_factory import dao_factory
from datetime import datetime, timezone, timedelta
from dotenv import load_dotenv


class BaseCollector:

    VALID_CONTENT_TYPES = ['media', 'github_projects']

    def validate_content_type_parameter(self, content_type):
        if content_type not in self.VALID_CONTENT_TYPES:
            raise ValueError(f"content_type must be one of {self.VALID_CONTENT_TYPES}")

    def __init__(self, creator_name: str, content_type, run_interval: timedelta = timedelta(days=1)):
        load_dotenv()
        self.validate_content_type_parameter(content_type)

        self.creator_name = creator_name
        self.table_name = f"t_{content_type}"
        self.content_type = content_type
        self.run_interval = run_interval

        self.dao = dao_factory()

    def get_latest_message_date(self):
        # Get date from the latest message to the telegram table - using topic / reporter
        result = self.dao.get_latest_data_date(self.creator_name, self.table_name)

    def retrieve(self):
        # Get data from the source
        raise NotImplementedError

    def convert_to_media(self, data):
        # Convert data to media object
        raise NotImplementedError

    def save(self, data):
        if isinstance(data, Collection) and not isinstance(data, str):
            result = []
            for item in data:
                result.append(self._convert_and_save(item))
            return result
        else:
            return self._convert_and_save(data)

    def _convert_and_save(self, data):
        media = self.convert_to_media(data)
        if media:
            result = self.dao.save(media)
            return result
        else:
            return None

    def is_due(self):
        lastest_data_date = self.dao.get_latest_data_date(self.creator_name, self.table_name).astimezone(timezone.utc)
        now = datetime.now(timezone.utc)
        time_diff = now - lastest_data_date

        if time_diff < self.run_interval:
            total_seconds = time_diff.total_seconds()
            hours = int(total_seconds // 3600)
            minutes = int((total_seconds % 3600) // 60)
            print(f"Weniger als 24 Stunden seit der letzten Nachricht vergangen: "
                  f"Vergangen bisher: {hours:02d}:{minutes:02d}")
            return False
        return True

    def run(self):
        if self.is_due():
            data = self.retrieve()
            self.save(data=data)
