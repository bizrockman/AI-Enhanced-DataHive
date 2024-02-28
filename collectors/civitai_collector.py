import os
from dotenv import load_dotenv
from urllib.parse import urlencode, urljoin

from collectors import BaseCollector
from collectors.utils.scraping_helper import get_request_as_json

from models import Media


class CivitaiCollector(BaseCollector):

    VALID_PERIODS = ['AllTime', 'Year', 'Month', 'Week', 'Day']
    VALID_MEDIA_TYPES = ['image', 'video', 'model']
    VALID_NSFW_LEVELS = [None, 'Soft', 'Mature', 'X']
    VALID_SORTS = ['Most Reactions', 'Most Buzz', 'Most Comments', 'Most Collected', 'Oldest']

    def __init__(self, creator_name='CivitaiCollector', media_type='image', period='Day', sort='Most Reactions',
                 nsfw=None, tags=None, limit=1):
        self.creator_name = creator_name
        if tags is None:
            self.tags = self.build_tags(media_type, period, sort, nsfw)
        else:
            self.tags = tags
        self.limit = limit

        self.validate_parameters(media_type, period, nsfw, sort)

        # TODO Right now, there is no way to determine videos directly from Civitai API
        # START - Workaround as long as there is no way to get videos directly from Civitai
        if media_type == 'video':
            self.media_type = 'image'
        else:
            self.media_type = media_type
        # END - Workaround as long as there is no way to get videos directly from Civitai

        base_url = os.getenv('CIVITAI_API_URL', '')
        self.civitai_url = self.build_url(base_url, media_type, sort, nsfw, period, limit)

        super().__init__(creator_name=self.creator_name, content_type=media_type, tags=tags)

    def build_tags(self, media_type, period, sort, nsfw):
        tags = 'civitai, '
        tags += media_type.lower() + ', '
        if period == 'Day':
            tags += 'daily, '
        elif period == 'Week':
            tags += 'weekly, '
        elif period == 'Month':
            tags += 'monthly, '
        elif period == 'Year':
            tags += 'yearly, '
        elif period == 'AllTime':
            tags += 'all time, '

        tags += sort.lower() + ', '
        if nsfw:
            tags += nsfw.lower() + ', '

        tags = tags.rstrip(', ')
        return tags

    def validate_parameters(self, media_type, period, nsfw, sort):
        if period not in self.VALID_PERIODS:
            raise ValueError(f"period must be one of {self.VALID_PERIODS}")
        if media_type not in self.VALID_MEDIA_TYPES:
            raise ValueError(f"media_type must be one of {self.VALID_MEDIA_TYPES}")
        if nsfw not in self.VALID_NSFW_LEVELS:
            raise ValueError(f"nsfw must be one of {self.VALID_NSFW_LEVELS}")
        if sort not in self.VALID_SORTS:
            raise ValueError(f"sort must be one of {self.VALID_SORTS}")

    def build_url(self, base_url, media_type, sort, nsfw, period, limit):
        path = f"{media_type}s"  # Append 's' to make it plural (image -> images, video -> videos, model -> models)
        params = {
            'nsfw': nsfw,
            'limit': limit,
            'period': period,
            'sort': sort
        }
        query_string = urlencode({k: v for k, v in params.items() if v is not None})  # Exclude None values
        return urljoin(base_url, path) + '?' + query_string

    def retrieve(self):
        data = get_request_as_json(self.civitai_url)

        if isinstance(data, dict):
            return data
        else:
            # Fehlerbehandlung
            print(f"Es gab einen Fehler bei der Anfrage: {data}")

    def convert_to_media(self, data):
        data = data['items'][0]

        if data:
            media = Media(
                creator=self.creator_name,
                media_url=data['url'],
                media_type=self.media_type,
                likes=data['stats']['likeCount'],
                hearts=data['stats']['heartCount'],
                prompt= data['meta']['prompt'],
                model=data['meta']['Model'].split('.')[0],
                author=data['username'],
                tags=self.tags,
                source='Civitai',
                media_created_at=data['createdAt']
            )

            return media


def main():
    load_dotenv()
    civitai_collector = CivitaiCollector(nsfw='X')
    #result = civitai_collector.save()
    data = civitai_collector.retrieve()
    print(data)
    media = civitai_collector.convert_to_media(data)

    print(media)


if __name__ == "__main__":
    main()
