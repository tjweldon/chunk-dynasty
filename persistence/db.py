import psycopg2

_con = None


def get_cursor():
    global _con
    if _con is None:
        _con = psycopg2.connect(database="postgres", user="postgres", password="Kaliakakya", host="db", port="5432")
    return _con.cursor()


def commit():
    _con.commit()


def close():
    con.commit()
    con.close()
