import sqlite3

class DbHandler:
    """handles database operation."""

    def __init__(self):
        self.connection = sqlite3.connect("./cogs/market/profiles.db")
        self.cur = self.connection.cursor()

    def register(self, id):
        """register a user with `id` into the database."""
        sql_command = """INSERT INTO profiles (id, xp, level) VALUES (?,?,?);"""
        self.cur.execute(sql_command, (id, 0, "None")) # start with no level; it's awarded at 1xp
        self.connection.commit()

    def exists(self, id):
        """return True if a user with `id` already exists, otherwise False."""
        sql_command = "SELECT EXISTS(SELECT 1 FROM profiles WHERE id = ?);"
        result = self.cur.execute(sql_command, (id,)).fetchone() # return 1 if it exists, otherwise 0
        return True if result[0] else False

    def update_xp(self, id, amount):
        """change the xp value of `id` by `amount`."""
        sql_command = "UPDATE profiles SET xp = xp + ? WHERE id = ?"
        self.cur.execute(sql_command, (amount, id))
        self.connection.commit()

    def update_level(self, id, new):
        """change the level of `id` to `new`."""
        sql_command = "UPDATE profiles SET level = ? WHERE id = ?"
        self.cur.execute(sql_command, (new, id))
        self.connection.commit()

    def profile_information(self, id):
        """return a dict containing information about the
           provided `id` in the format {"id": id, "xp": xp, "level": level}"""
        sql_command = "SELECT * FROM profiles WHERE id = ?"
        result = self.cur.execute(sql_command, (id,)).fetchone() # return tuple (id, level, xp)
        return {"id": id, "xp": result[2], "level": result[1]}

    def reset(self):
        """drop the table and replace it with a clean one.  use this very sparingly."""
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
