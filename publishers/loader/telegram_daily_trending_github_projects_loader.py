from transformers.models import Content

from publishers.loader import TelegramBaseLoader
from utils.datetime_helper import today_as_start_and_enddate_str


class TelegramDailyTrendingGithubProjectsLoader(TelegramBaseLoader):
    def __init__(self, telegram_group_name, telegram_group_topic_id):
        super().__init__(telegram_group_name, telegram_group_topic_id)

    def retrieve(self):
        start_date_str, end_date_str = today_as_start_and_enddate_str()
        filters = [
            ["creator", "DailyTrendingGithubProjects"],
            ["language", "de"],
            ["created_at", "between", start_date_str, end_date_str]
        ]

        projects = self.dao.read(Content, filters, limit=1)
        return projects[0]


def main():
    from dotenv import load_dotenv
    load_dotenv()
    ARXIV_GROUP_TOPIC_ID = 20
    loader = TelegramDailyTrendingGithubProjectsLoader('KI & Business', ARXIV_GROUP_TOPIC_ID)
    loader.load()


if __name__ == '__main__':
    main()
