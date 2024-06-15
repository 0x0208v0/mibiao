import logging

logger = logging.getLogger(__name__)


def crawl_post():
    logger.info(f'crawl_post start!')
    try:

        from mibiao.app import app
        from mibiao.models import db
        from mibiao.models.post import Post

        with app.app_context():
            Post.crawl()
            db.session.close_all()

    except Exception as e:
        logger.error(f'{e}')

    logger.info(f'crawl_post done!')


if __name__ == '__main__':
    logger.info = print
    crawl_post()
