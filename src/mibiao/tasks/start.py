from apscheduler.schedulers.blocking import BlockingScheduler

from mibiao.tasks.post import crawl_post


def main():
    scheduler = BlockingScheduler()

    scheduler.add_job(crawl_post, 'interval', seconds=10, kwargs={})

    scheduler.start()


if __name__ == '__main__':
    main()
