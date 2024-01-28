import pymysql
from config import user, host, password, db_name


class Database:
    def __init__(self):
        self.connection = pymysql.connect(
            host=host,
            port=3306,
            user=user,
            password=password,
            database=db_name,
            cursorclass=pymysql.cursors.DictCursor
        )
        self.cursor = self.connection.cursor()

    async def add_queue(self, chat_id):
        return self.cursor.execute(f"INSERT INTO `queue` (`chat_id`)"
                                   f"VALUES ({chat_id})")

    async def delete_queue(self, chat_id):
        return self.cursor.execute(f"DELETE FROM `queue` WHERE `chat_id` = {chat_id}")

    async def delete_chat(self, id_chat):
        return self.cursor.execute(f"DELETE FROM `chats` WHERE `id` = {id_chat}")

    async def get_chat(self):
        self.cursor.execute("SELECT * FROM `queue`")
        chat = self.cursor.fetchmany(1)
        if len(chat):
            for row in chat:
                print(row)
                return int(row['chat_id'])
        else:
            return False

    async def create_chat(self, chat_one, chat_two):
        if chat_two:
            # Создание чата
            await self.delete_queue(chat_two)
            self.cursor.execute("INSERT INTO `chats` (`chat_one`, `chat_two`)"
                                f"VALUES ({chat_one}, {chat_two})")
            return True
        else:
            # Становимся в очередь
            return False

    async def get_active_chat(self, chat_id):
        self.cursor.execute(f"SELECT * FROM `chats` WHERE `chat_one` = {chat_id}")
        chat = self.cursor.fetchall()
        id_chat = 0
        for row in chat:
            print(row)
            id_chat = row['id']
            chat_info = [row['id'], row['chat_two']]
        if id_chat == 0:
            self.cursor.execute(f"SELECT * FROM `chats` WHERE `chat_two` = {chat_id}")
            chat = self.cursor.fetchall()
            for row in chat:
                id_chat = row['id']
                chat_info = [row['id'], row['chat_one']]
            if id_chat == 0:
                return False
            else:
                return chat_info
        else:
            return chat_info
