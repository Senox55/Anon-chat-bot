import pymysql
from config import user, host, password, db_name


class Database:
    def __init__(self, database_file):
        self.connection = pymysql.connect(database_file)
        self.cursor = self.connection.cursor()

    def add_queue(self, chat_id):
        with self.connection:
            return self.cursor.execute("INSERT INTO `queue` (`chat_id`) VALUES (?)", (chat_id,))
