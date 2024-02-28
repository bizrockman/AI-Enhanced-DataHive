import os

from dotenv import load_dotenv
from datetime import datetime, timezone

from models import Media
from collectors import BaseCollector
import collectors.utils.arxiv_helper as ah


class ArxivCollector(BaseCollector):

    VALID_PERIODS = ['Day']

    def __init__(self, creator_name='ArxivCollector', arxiv_category='cs.AI', period='Day', tags=None, limit=3):
        self.creator_name = creator_name
        self.limit = limit
        self.arxiv_category = arxiv_category
        self.period = period
        self.media_type = 'paper'

        if tags is None:
            self.tags = self.build_tags(arxiv_category, period)
        else:
            self.tags = tags

        self.validate_parameters(arxiv_category, period)

        super().__init__(self.creator_name, content_type=self.media_type)

    def validate_parameters(self, arxiv_category, period):
        if arxiv_category not in ah.ALL_CATEGORIES:
            raise ValueError(f"category must be one of {ah.ALL_CATEGORIES}")
        if period not in self.VALID_PERIODS:
            raise ValueError(f"period must be one of {self.VALID_PERIODS}")

    def build_tags(self, arxiv_category, period):
        tags = 'arxiv, '
        tags += arxiv_category.lower() + ', '
        if period == 'Day':
            tags += 'daily, '

        tags = tags.rstrip(', ')
        return tags

    def retrieve(self):
        entries = ah.do_today_search(self.arxiv_category, self.limit)
        return entries

    def convert_to_media(self, data):
        if data:
            if 'Remaining Information' in data['title']:
                media = Media(
                    creator=self.creator_name,
                    media_type=self.media_type,
                    title=data['title'],
                    description=data['description'],
                    tags=self.tags + ', count',
                    source='Arxiv',
                    media_created_at=datetime.now(timezone.utc),
                    # TODO rework function call
                    reference_url=ah.search_day_submissions(self.arxiv_category, os.getenv('ARXIV_RSS_LINK'))
                )
            else:
                now = datetime.now(timezone.utc)
                media = Media(
                    creator=self.creator_name,
                    media_type=self.media_type,
                    title=data['title'],
                    description=data['description'],
                    author=data['authors'],
                    tags=self.tags,
                    source='Arxiv',
                    media_created_at=now,
                    reference_url=data['link']
                )

            return media


def main():
    load_dotenv()
    arxiv_collector = ArxivCollector()
    data = arxiv_collector.retrieve()
    result = arxiv_collector.save(data)
    print(result)
    #media = civitai_collector.convert_to_media(data)

    #print(media)


if __name__ == "__main__":
    main()
