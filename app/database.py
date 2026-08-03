import sqlite3


class Database:

    def __init__(self):

        self.conn = sqlite3.connect(
            "data/database.db",
            check_same_thread=False
        )

        self.cursor = self.conn.cursor()

        self.create_students_table()
        self.create_attendance_table()


    # ==================================
    # STUDENTS TABLE
    # ==================================

    def create_students_table(self):

        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS students(

            student_id TEXT PRIMARY KEY,

            name TEXT NOT NULL,

            department TEXT,

            year TEXT,

            section TEXT,

            embedding BLOB NOT NULL
        )
        """)

        self.conn.commit()



    # ==================================
    # ATTENDANCE TABLE
    # ==================================

    def create_attendance_table(self):

        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS attendance(

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            student_id TEXT,

            name TEXT,

            date TEXT,

            time TEXT,

            status TEXT,

            UNIQUE(student_id,date)

        )
        """)

        self.conn.commit()



    # ==================================
    # ADD STUDENT
    # ==================================

    def add_student(
        self,
        student_id,
        name,
        department,
        year,
        section,
        embedding
    ):

        self.cursor.execute("""
        INSERT OR REPLACE INTO students
        (
            student_id,
            name,
            department,
            year,
            section,
            embedding
        )

        VALUES(?,?,?,?,?,?)

        """,
        (
            student_id,
            name,
            department,
            year,
            section,
            embedding
        ))


        self.conn.commit()



    # ==================================
    # GET STUDENTS
    # ==================================

    def get_students(self):

        self.cursor.execute("""
        SELECT 
        student_id,
        name,
        department,
        year,
        section,
        embedding

        FROM students
        """)

        return self.cursor.fetchall()



    # ==================================
    # CHECK TODAY ATTENDANCE
    # ==================================

    def already_marked(
        self,
        student_id,
        date
    ):

        self.cursor.execute("""
        SELECT *
        FROM attendance

        WHERE student_id=?
        AND date=?

        """,
        (
            student_id,
            date
        ))


        result = self.cursor.fetchone()


        if result:
            return True

        return False



    # ==================================
    # MARK ATTENDANCE
    # ==================================

    def mark_attendance(
        self,
        student_id,
        name,
        date,
        time,
        status
    ):


        if self.already_marked(
            student_id,
            date
        ):

            return False



        self.cursor.execute("""
        INSERT INTO attendance
        (
            student_id,
            name,
            date,
            time,
            status
        )

        VALUES(?,?,?,?,?)

        """,
        (
            student_id,
            name,
            date,
            time,
            status
        ))


        self.conn.commit()


        return True



    # ==================================
    # GET ATTENDANCE
    # ==================================

    def get_attendance(self):


        self.cursor.execute("""
        SELECT

        id,
        student_id,
        name,
        date,
        time,
        status

        FROM attendance

        ORDER BY id DESC

        """)


        return self.cursor.fetchall()



    # ==================================
    # TOTAL STUDENTS
    # ==================================

    def count_students(self):

        self.cursor.execute(
            "SELECT COUNT(*) FROM students"
        )

        return self.cursor.fetchone()[0]



    # ==================================
    # TODAY ENTRIES
    # ==================================

    def today_entries(self,date):

        self.cursor.execute("""
        SELECT COUNT(*)

        FROM attendance

        WHERE date=?

        """,
        (date,))


        return self.cursor.fetchone()[0]



    # ==================================
    # CLOSE DATABASE
    # ==================================

    def close(self):

        self.conn.close()