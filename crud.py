import sqlite3


class CRUD:
    def __init__(self, db_name):
        """
        :param db_name: the database name to connect, if it's new, this make the database
        """
        self.connection = sqlite3.connect(db_name)
        self.cursor = self.connection.cursor()

    def create(self, column, header, data):
        """
        this function is used to insert data in database
        :param column: table to insert data
        :param header: values that have the table
        :param data: data to add, must be an array
        :return: boolean that lets u know if it works correctly
        """
        query = f"insert into {column} ({header}) values (" + ", ".join("?" for _ in range(len(data))) + ")"

        try:
            self.cursor.execute(query, data)
            self.connection.commit()
            return 1
        except sqlite3.Error as e:
            print(e)
            return 0

    def read(self, column, header):
        """
        this function is used to read data in database
        :param column: table to read data
        :param header: table values u want
        :return: values
        """
        try:
            data = self.cursor.execute(f"select {header} from {column}")
            data = data.fetchall()

            return data

        except sqlite3.Error as e:
            print(e)
            return False

    def read_with_id(self, id_, header, column):
        """
        this function is used to read with id in database
        :param id_: the ID to search
        :param header: table to read data
        :param column: table values u want
        :return: searched value, 1 _if can't find out, none if exists error
        """
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
        """
        this function is used to update data in database
        :param column: table to update
        :param header: table values
        :param id_: from table to update
        :param data: data new
        :return: TRUE if updated correctly, else FALSE
        """
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
        """
        this function is used to delete data in database
        :param column: table to delete
        :param id_: from table to delete
        :return: TRUE if deleted correctly, else FALSE
        """
        try:
            self.cursor.execute(f"delete from {column} where id = {id_}")
            self.connection.commit()
            return True

        except sqlite3.Error as e:
            print(e)
            return False

    def init_db(self):
        """
        this function is used to create the database columns
        """
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
