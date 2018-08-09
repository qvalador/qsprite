import sqlite3

class DbHandler:
    """handles database operation."""

    def __init__(self):
        self.connection = sqlite3.connect("./cogs/market/profiles.db")
        self.cur = self.connection.cursor()

    def register(self, id):
        """registers a user with @id in the database."""
        sql_command = """INSERT INTO profiles (id, xp, level) VALUES (?,?,?);"""
        self.cur.execute(sql_command, (id, 0, "None"))
        self.connection.commit()

    def exists(self, id):
        """returns true if a user with @id already exists, otherwise false."""
        sql_command = "SELECT EXISTS(SELECT 1 FROM profiles WHERE id = ?);"
        result = self.cur.execute(sql_command, (id,)).fetchone()
        return True if result[0] else False

    def update_xp(self, id, amount):
        """changes the xp value of @id by @amount."""
        symbol = "+" if amount >= 0 else "-"
        sql_command = "UPDATE profiles SET xp = xp ? ? WHERE id = ?"
        self.cur.execute(sql_command, (symbol, amount, id))
        self.connection.commit()

    def update_level(self, id, new):
        """changes the level of @id to @new."""
        sql_command = "UPDATE profiles SET level = ? WHERE id = ?"
        self.cur.execute(sql_command, (new, id))
        self.connection.commit()

    def profile_information(self, id):
        """returns a dict containing information about the
           provided @id in the format {"id": id, "xp": xp, "level": level}"""
        sql_command = "SELECT * FROM profiles WHERE id = ?"
        result = self.cur.execute(sql_command, (id,)).fetchone()
        return {"id": id, "xp": result[2], "level": result[1]}

    def reset(self):
        """drops the table and replaces it with a clean one.  use this very sparingly."""
        self.cur.execute("DROP TABLE profiles;")
        sql_command = """
                        CREATE TABLE profiles (
                        id INTEGER,
                        level TEXT,
                        xp INTEGER,
                        PRIMARY KEY (id)
                        );"""
        self.cur.execute(sql_command)
        self.connection.commit()
