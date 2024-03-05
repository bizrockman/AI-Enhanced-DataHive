from transformers.models import Content

from utils.datetime_helper import today_as_start_and_enddate_str

from publishers.models import TelegramMessage, TelegramGroup, TelegramGroupTopic


class TopDailyImageLoader:

    def __init__(self, telegram_group_name, telegram_group_topic_id):
        from dao.dao_factory import dao_factory
        self.dao = dao_factory()

        tgr = self.dao.read(TelegramGroup, [["telegram_group_name", telegram_group_name]], limit=1)
        if not tgr:
            raise ValueError(f"Telegram-Gruppe '{telegram_group_name}' nicht gefunden.")

        self.telegram_group_uuid = tgr[0].id
        self.telegram_group_topic_id = telegram_group_topic_id

    def retrieve(self):
        start_date_str, end_date_str = today_as_start_and_enddate_str()
        filters = [
            ["creator", "TopDailyImage"],
            ["language", "de"],
            ["created_at", "between", start_date_str, end_date_str]
        ]

        topimage = self.dao.read(Content, filters, limit=1)
        return topimage[0]

    def find_group_topic_uuid(self):
        filters = [
            ["telegram_group_topic_id", self.telegram_group_topic_id],
            ["telegram_group_fk", self.telegram_group_uuid]
        ]

        group_topic = self.dao.read(TelegramGroupTopic, filters, limit=1)
        if group_topic:
            return group_topic[0].id
        else:
            return None

    def save_content_as_telegram_message(self, content: Content):
        group_topic_uuid = self.find_group_topic_uuid()
        if not group_topic_uuid:
            print("Keine entsprechende group_topic_id gefunden.")
            return

        # Datenstruktur für die neue Nachricht
        message_data = {
            'telegram_group_topic_fk': group_topic_uuid,
            'content': f"<b>{content.title}</b>\n{content.content}",
            'creator': content.creator,
            'status': 'planned'
        }

        if content.media_type and (content.media_url or content.media_content):
            message_data['media_type'] = content.media_type
            if content.media_url:
                message_data['media_url'] = content.media_url
            elif content.media_content:
                message_data['media_content'] = content.media_content

        # Füge `schedule_for` hinzu, wenn ein Zeitpunkt angegeben ist
        if content.scheduled_for:
            message_data['schedule_for'] = content.schedule_for

        # Speichern der Nachricht in der Tabelle `t_telegram_messages`
        result = self.dao.create(TelegramMessage(**message_data))

    def load(self):
        content = self.retrieve()
        self.save_content_as_telegram_message(content)


def main():
    from dotenv import load_dotenv
    load_dotenv()
    loader = TopDailyImageLoader('KI & Business', 27)
    loader.load()


if __name__ == '__main__':
    main()
