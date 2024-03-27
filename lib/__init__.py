# lib/config.py
import sqlite3

CONN = sqlite3.connect('company.db')
CURSOR = CONN.cursor()



class Review:
    def __init__(self, year, summary, employee_id, id_=None):
        self.id = id_
        self.year = year
        self.summary = summary
        self.employee_id = employee_id

    def __repr__(self):
        return f"Review(id={self.id}, year={self.year}, summary={self.summary}, employee_id={self.employee_id})"

    
    def create_table(cls):
        CURSOR.execute('''CREATE TABLE IF NOT EXISTS reviews
                          (id INTEGER PRIMARY KEY,
                           year INTEGER,
                           summary TEXT,
                           employee_id INTEGER,
                           FOREIGN KEY (employee_id) REFERENCES employees(id))''')
        CONN.commit()

    
    def drop_table(cls):
        CURSOR.execute('DROP TABLE IF EXISTS reviews')
        CONN.commit()

    def save(self):
        if self.id is None:
            CURSOR.execute('''INSERT INTO reviews (year, summary, employee_id)
                              VALUES (?, ?, ?)''', (self.year, self.summary, self.employee_id))
            self.id = CURSOR.lastrowid
            CONN.commit()
        else:
            CURSOR.execute('''UPDATE reviews
                              SET year=?, summary=?, employee_id=?
                              WHERE id=?''', (self.year, self.summary, self.employee_id, self.id))
            CONN.commit()

   
    def create(cls, year, summary, employee_id):
        review = cls(year, summary, employee_id)
        review.save()
        return review

    def instance_from_db(cls, row):
        review_id, year, summary, employee_id = row
        review = cls(year, summary, employee_id, id_=review_id)
        return review

  
    def find_by_id(cls, review_id):
        CURSOR.execute('''SELECT * FROM reviews WHERE id=?''', (review_id,))
        row = CURSOR.fetchone()
        if row:
            return cls.instance_from_db(row)
        else:
            return None

    def update(self):
        self.save()

    def delete(self):
        CURSOR.execute('''DELETE FROM reviews WHERE id=?''', (self.id,))
        CONN.commit()
        self.id = None

  
    def get_all(cls):
        CURSOR.execute('''SELECT * FROM reviews''')
        rows = CURSOR.fetchall()
        return [cls.instance_from_db(row) for row in rows]

    
    def year(self):
        return self._year

    @year.setter
    def year(self, value):
        if not isinstance(value, int) or value < 2000:
            raise ValueError("Year must be an integer greater than or equal to 2000")
        self._year = value


    def summary(self):
        return self._summary


    def summary(self, value):
        if not isinstance(value, str) or len(value.strip()) == 0:
            raise ValueError("Summary must be a non-empty string")
        self._summary = value

    
    def employee_id(self):
        return self._employee_id

    
    def employee_id(self, value):
        if not isinstance(value, int):
            raise ValueError("Employee ID must be an integer")
   
        self._employee_id = value
