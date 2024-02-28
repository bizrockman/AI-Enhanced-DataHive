import os

from dotenv import load_dotenv
from collectors import BaseCollector

from collectors.utils.allowed_github_parameter import AllowedDateRanges
from collectors.utils.scraping_helper import get_request
from collectors.utils.github_helper import filter_articles, make_soup, scraping_repositories

from models import GithubProject

from utils import datetime_helper as dh


class GithubCollector(BaseCollector):

    VALID_PERIODS = ['Day', 'Week', 'Month']

    #TODO if needed use more parameters, right now fixed to github trending repos
    def __init__(self, creator_name='GithubCollector', period='Day', tags=None, limit=3):
        self.creator_name = creator_name
        self.limit = limit
        self.period = period
        self.media_type = 'github_project'
        self.github_url = os.getenv('GITHUB_TRENDS_URL')

        if tags is None:
            self.tags = self.build_tags(period)
        else:
            self.tags = tags

        self.validate_parameters(period)

        super().__init__(self.creator_name, content_type=self.media_type, table_name='t_github_projects')

    def validate_parameters(self, period):
        if period not in self.VALID_PERIODS:
            raise ValueError(f"period must be one of {self.VALID_PERIODS}")

    def build_tags(self, period):
        tags = 'github, '
        tags += 'trending, '
        tags += dh.to_periodic_format(period) + ', '

        tags = tags.rstrip(', ')
        return tags

    def trending_repositories(self, since: AllowedDateRanges = None):
        """Returns data about trending repositories (all programming
        languages, cannot be specified on this endpoint)."""
        if since:
            payload = {"since": since}
        else:
            payload = {"since": "weekly"}

        raw_html = get_request(self.github_url, payload)

        articles_html = filter_articles(raw_html)
        soup = make_soup(articles_html)
        return scraping_repositories(soup, since=payload[
            "since"])

    def retrieve(self):
        periodicity = dh.to_periodic_format(self.period)
        entries = self.trending_repositories(since=periodicity)
        return entries[:self.limit]

    def convert_to_media(self, data):
        if data:
            contributors = [user['username'] for user in data['builtBy']]

            # Format output
            if len(contributors) > 3:
                output = ', '.join(contributors[:3]) + ', et al.'
            else:
                output = ', '.join(contributors)

            project = GithubProject(
                creator=self.creator_name,
                username=data['username'],
                name=data['repositoryName'],
                url=data['url'],
                description=data['description'],
                program_language=data['language'],
                language=data['language'],
                total_stars=data['totalStars'],
                forks=data['forks'],
                new_stars=data['starsSince'],
                since=data['since'],
                tags=self.tags,
                contributors=output
            )

            return project


def main():
    load_dotenv()
    github_collector = GithubCollector()
    data = github_collector.retrieve()
    result = github_collector.save(data)
    print(result)


if __name__ == "__main__":
    main()
