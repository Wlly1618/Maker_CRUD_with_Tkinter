import sqlite3


class CRUD:
    def __init__(self, db_name):
        pass
        self.connection = sqlite3.connect(db_name)
        self.cursor = self.connection.cursor()

    def create(self, column, header, data):
        placeholders = ", ".join("?" for _ in range(len(data)))
        query = f"insert into {column} ({header}) values ({placeholders})"

        # print(query)

        try:
            self.cursor.execute(query, data)
            self.connection.commit()
            return 1
        except sqlite3.Error as e:
            print(e)
            return 0

    def read(self, column, header):
        try:
            data = self.cursor.execute(f"select {header} from {column}")
            data = data.fetchall()

            return data

        except sqlite3.Error as e:
            print(e)
            return 0

    def read_with_id(self, id_, header, column):
        try:
            data = self.cursor.execute(f"select {header} from {column} where id = {id_}")
            data = data.fetchall()

            if data:
                return data
            else:
                return 1

        except sqlite3.Error as e:
            print(e)
            return None

    def update_(self, column, header, id_, data):
        placeholders = ", ".join(f"{head}=?" for head in header)

        query = f"update {column} set {placeholders} where id = ?"
        data.append(id_)

        try:
            self.cursor.execute(query, data)
            self.connection.commit()
            return True
        except sqlite3.Error as e:
            print(e)
            return False

    def delete_(self, column, id_):
        try:
            self.cursor.execute(f"delete from {column} where id = {id_}")
            self.connection.commit()
            return True

        except sqlite3.Error as e:
            print(e)
            return False

    def init_db(self):
        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS product (
                id INTEGER PRIMARY KEY,
                price FLOAT,
                name VARCHAR(50),
                stock INTEGER
            )
            """
        )

        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS client (
                id INTEGER PRIMARY KEY,
                name VARCHAR(50)
            )
            """
        )

        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS shop (
                id INTEGER PRIMARY KEY,
                date DATE,
                id_client INTEGER,
                FOREIGN KEY (id_client) REFERENCES client(id)
            )
            """
        )

        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS detail (
                id INTEGER PRIMARY KEY,
                amount INTEGER,
                id_shop INTEGER,
                id_product INTEGER,
                FOREIGN KEY (id_shop) REFERENCES shop(id),
                FOREIGN KEY (id_product) REFERENCES product(id)
            )
            """
        )

        self.connection.commit()
