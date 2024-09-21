from collections import OrderedDict


class Utils:
    def dict_fetch_all(cursor):
        columns = [col[0] for col in cursor.description]
        return [OrderedDict(zip(columns, row)) for row in cursor.fetchall()]
