import logging
from datetime import datetime, timezone

import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

logging.basicConfig(level=logging.DEBUG)


class Db_Singletone:
    def __init__(self):
        with psycopg2.connect(user="postgres",
                              password="unlimitedpower",
                              host="127.0.0.1",
                              port="5432",
                              database="chan") as self.connection:
            self.connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
            self.cursor = self.connection.cursor()

    def __del__(self):
        if self.connection:
            self.cursor.close()
            self.connection.close()
            logging.critical("Соединение с PostgreSQL закрыто")

    def get_boards(self):
        self.cursor.execute("SELECT id FROM boards;")
        record = self.cursor.fetchall()
        record = list(x[0] for x in record)
        return record

    def get_boardname(self):
        self.cursor.execute("SELECT boardname FROM boards;")
        record = self.cursor.fetchall()
        record = list(x[0] for x in record)
        return record

    def get_threads(self, board):
        self.cursor.execute("select * from threads where board=%s;", (board,))
        record = self.cursor.fetchall()
        # record = list(x[0] for x in record)
        return record

    def create_thread(self, board, message, subject=None, ):
        dt = datetime.now(timezone.utc)
        self.cursor.execute("insert into threads (board, subject, message, timestamp)"
                            "values (%s, %s, %s, %s) returning id;", (board, subject, message, dt,))
        record = self.cursor.fetchall()
        record = list(x[0] for x in record)
        return record

    def get_root(self, board, thread, ):
        self.cursor.execute("select subject, message from threads where (board=%s and id=%s);", (board, thread,))
        record = self.cursor.fetchall()
        record = record[0]
        return record

    def get_posts(self, board, thread):
        self.cursor.execute("select * from posts where (board=%s and thread=%s);", (board, thread,))
        record = self.cursor.fetchall()
        # record = list(x[0] for x in record)
        return record

    def create_post(self, board, thread,  message):  # TODO attachments
        dt = datetime.now(timezone.utc)
        self.cursor.execute("insert into posts (board, thread, message, timestamp)"
                            "values (%s, %s, %s, %s );", (board, thread, message, dt))

    def get_news(self):
        self.cursor.execute("select * from news;")
        record = self.cursor.fetchall()
        # record = list(x[0] for x in record)
        return record

    def add_news(self, subject, article):
        dt = datetime.now(timezone.utc)
        self.cursor.execute("insert into news (subject, article, timestamp)"
                            "values (%s, %s, %s);", (subject, article, dt,))

    def update_news(self, new_subject, article, old_subject):
        self.cursor.execute("update news set (subject, article)"
                            "values (%s, %s)"
                            "where subject = %s;", (new_subject, article, old_subject,))

    def delete_news(self, subject):
        self.cursor.execute("delete from news where article=%s;", (subject,))


db_handler = Db_Singletone()
