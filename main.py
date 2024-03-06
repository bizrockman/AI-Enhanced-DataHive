import datetime
import time

from dotenv import load_dotenv

from collectors import CivitaiCollector

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore


def civitai_top_image_of_the_day_collector_job():
    civitai_image_loader = CivitaiCollector(creator_name='CivitAIDailyTopImage', media_type='image', period='Day',
                                            nsfw=None, limit=3)
    civitai_image_loader.run()
    civitai_hot_image_loader = CivitaiCollector(creator_name='CivitAIDailyTopHotImage', media_type='image',
                                                period='Day', nsfw='Mature', limit=3)
    civitai_hot_image_loader.run()


def main():
    load_dotenv()

    jobstores = {
        'default': SQLAlchemyJobStore(url='sqlite:///jobs.sqlite')
    }

    # Berechne die Startzeiten
    now = datetime.datetime.now()
    start_in_10_min = now + datetime.timedelta(minutes=10)
    start_in_30_min = now + datetime.timedelta(minutes=30)

    scheduler = BackgroundScheduler(jobstores=jobstores)
    scheduler.add_job(civitai_top_image_of_the_day_collector_job, 'interval', hours=1, next_run_time=now)
    scheduler.start()

    try:
        # Damit das Skript läuft, bis es manuell gestoppt wird
        while True:
            time.sleep(2)
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown()


if __name__ == "__main__":
    main()
