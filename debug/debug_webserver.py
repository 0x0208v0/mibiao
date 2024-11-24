from mibiao.app import app
from mibiao.models import db
from mibiao.models.domain import Domain
from mibiao.models.tag import Tag
from mibiao.models.user import User


def create_test_data():
    with app.app_context():
        db.drop_all()
        db.create_all()

        user = User(email='a@a.com', name='a', avatar_url='https://www.nodeseek.com/avatar/15068.png')
        user.password = 'a'

        tag = Tag(name='全部', url_path_name='', user=user)

        objs = [
            user,
            tag,
            Domain(
                user=user,
                name='a.com',
                description='这是一额米，现价100，续费100，赶紧买',
                tags=[tag],
            ),
            Domain(
                user=user,
                name='b.com',
                description='这是一额米',
            ),
            Domain(
                user=user,
                name='c.com',
            ),
        ]
        db.session.add_all(objs)
        db.session.flush()
        db.session.commit()


if __name__ == '__main__':
    # 如果需要测试数据，可以解除 create_test_data() 注释
    create_test_data()
    app.run(
        debug=True,
        threaded=False,
        host='localhost',
        port=15000,
    )
