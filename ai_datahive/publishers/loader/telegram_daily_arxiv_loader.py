from ai_datahive.transformers.models import Content

from ai_datahive.publishers.loader import TelegramBaseLoader
from ai_datahive.utils import datetime_helper


class TelegramDailyArxivLoader(TelegramBaseLoader):

    def __init__(self, telegram_group_name, telegram_group_topic_id, creator='TelegramDailyArxivLoader', language='de'):
        self.creator = creator
        self.language = language
        super().__init__(creator, language, telegram_group_name, telegram_group_topic_id)

    def retrieve(self):
        start_date_str, end_date_str = datetime_helper.today_as_start_and_enddate_str()
        filters = [
            ["creator", "DailyArxivPaper"],
            ["lang", self.language],
            ["created_at", "between", start_date_str, end_date_str]  # TODO extract from run_interval
        ]

        paper = self.dao.read(Content, filters, limit=1)
        if len(paper) > 0:
            return paper[0]
        return None


def main():
    from dotenv import load_dotenv
    load_dotenv()
    ARXIV_GROUP_TOPIC_ID = 2
    loader = TelegramDailyArxivLoader('KI & Business', ARXIV_GROUP_TOPIC_ID)
    loader.load()


if __name__ == '__main__':
    main()
