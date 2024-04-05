from dotenv import load_dotenv
from ai_datahive.publishers.loader import (TelegramDailyTrendingGithubProjectsLoader, TelegramDailyArxivLoader,
                                           TelegramTopDailyImageLoader, TelegramTopDailyImageCritiqueLoader)


def main():
    load_dotenv()

    ARXIV_GROUP_TOPIC_ID = 2
    PROJECTS_GROUP_TOPIC_ID = 20
    IMAGE_GROUP_TOPIC_ID = 27

    loader = TelegramDailyArxivLoader('KI & Business', ARXIV_GROUP_TOPIC_ID)
    loader.load()

    loader = TelegramDailyTrendingGithubProjectsLoader('KI & Business', PROJECTS_GROUP_TOPIC_ID)
    loader.load()

    loader = TelegramTopDailyImageCritiqueLoader('KI & Business', IMAGE_GROUP_TOPIC_ID)
    loader.load()

    loader = TelegramTopDailyImageLoader('KI & Business', IMAGE_GROUP_TOPIC_ID)
    loader.load()


if __name__ == '__main__':
    main()
