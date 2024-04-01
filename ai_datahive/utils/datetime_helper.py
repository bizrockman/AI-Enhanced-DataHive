from typing import Type
from datetime import datetime, timedelta, timezone

from ai_datahive.models import DataHiveBaseModel
from ai_datahive.dao.dao_factory import dao_factory


def to_periodic_format(period):
    if period == 'Day':
        return 'daily'
    elif period == 'Week':
        return 'weekly'
    elif period == 'Month':
        return 'monthly'
    elif period == 'Year':
        return 'yearly'
    elif period == 'AllTime':
        return 'all time'


def today_as_start_and_enddate_str(pattern='%Y-%m-%d'):
    today = datetime.now().date()
    start_date = today
    end_date = today + timedelta(days=1)
    start_date_str = start_date.strftime(pattern)
    end_date_str = end_date.strftime(pattern)

    return start_date_str, end_date_str


def is_due(content_type: Type[DataHiveBaseModel], creator_name, run_interval):
    if content_type is None:
        raise NotImplementedError('If no content_type is defined, you have to implement this method.')

    dao = dao_factory()
    latest_entity_date = dao.get_latest_entity_date(content_type, creator_name)

    if latest_entity_date is None:
        return True

    latest_entity_date = latest_entity_date.astimezone(timezone.utc)
    now = datetime.now(timezone.utc)
    time_diff = now - latest_entity_date

    if time_diff < run_interval:
        total_seconds = time_diff.total_seconds()
        hours = int(total_seconds // 3600)
        minutes = int((total_seconds % 3600) // 60)
        print(f"Weniger als 24 Stunden seit der letzten Nachricht vergangen: "
              f"Vergangen bisher: {hours:02d}:{minutes:02d}")
        return False
    return True
