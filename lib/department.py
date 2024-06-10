# department.py

from __init__ import CONN, CURSOR

class Department:
    all = {}

    def __init__(self, name, location):
        self.id = None
        self.name = name
        self.location = location

    @classmethod
    def create_table(cls):
        sql = """
        CREATE TABLE IF NOT EXISTS departments (
            id INTEGER PRIMARY KEY,
            name TEXT,
            location TEXT
        )
        """
        CURSOR.execute(sql)
        CONN.commit()

    @classmethod
    def drop_table(cls):
        sql = "DROP TABLE IF EXISTS departments"
        CURSOR.execute(sql)
        CONN.commit()

    def save(self):
        if self.id is None:
            sql = """
            INSERT INTO departments (name, location)
            VALUES (?, ?)
            """
            CURSOR.execute(sql, (self.name, self.location))
            self.id = CURSOR.lastrowid
        else:
            sql = """
            UPDATE departments
            SET name = ?, location = ?
            WHERE id = ?
            """
            CURSOR.execute(sql, (self.name, self.location, self.id))
        CONN.commit()

    @classmethod
    def create(cls, name, location):
        department = cls(name, location)
        department.save()
        cls.all[department.id] = department
        return department

    def update(self):
        sql = """
        UPDATE departments
        SET name = ?, location = ?
        WHERE id = ?
        """
        CURSOR.execute(sql, (self.name, self.location, self.id))
        CONN.commit()

    def delete(self):
        sql = """
        DELETE FROM departments
        WHERE id = ?
        """
        CURSOR.execute(sql, (self.id,))
        CONN.commit()
        Department.all.pop(self.id, None)
        self.id = None  # Set the id to None after deletion

    @classmethod
    def instance_from_db(cls, row):
        department = cls(row[1], row[2])
        department.id = row[0]
        return department

    @classmethod
    def get_all(cls):
        sql = "SELECT * FROM departments"
        rows = CURSOR.execute(sql).fetchall()
        return [cls.instance_from_db(row) for row in rows]

    @classmethod
    def find_by_id(cls, id):
        sql = "SELECT * FROM departments WHERE id = ?"
        row = CURSOR.execute(sql, (id,)).fetchone()
        if row:
            return cls.instance_from_db(row)
        return None

    @classmethod
    def find_by_name(cls, name):
        sql = "SELECT * FROM departments WHERE name = ?"
        row = CURSOR.execute(sql, (name,)).fetchone()
        if row:
            return cls.instance_from_db(row)
        return None

    def employees(self):
        from employee import Employee  # avoid circular import issue
        sql = "SELECT * FROM employees WHERE department_id = ?"
        rows = CURSOR.execute(sql, (self.id,)).fetchall()
        return [Employee.instance_from_db(row) for row in rows]
