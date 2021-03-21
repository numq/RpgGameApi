import datetime


class SqlAlchemyUtils:

    def datetime_sqlalchemy(self, value):
        return datetime.datetime.strptime(value, '%Y-%m-%d %H:%M:%S')
