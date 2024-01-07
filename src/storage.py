import sqlite3
from datetime import datetime
from proc import Proc
from logger import Logger

logger = Logger()

class Storage:
    def __init__(self, basepath: str) -> None:  
        self.db = None      
        date = datetime.now().strftime("%Y%m%d")

        try:
            self.db = sqlite3.connect(f"{basepath}//{date}.db")
            cursor = self.db.cursor()

            cursor.execute("""
CREATE TABLE IF NOT EXISTS processes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,                
    name TEXT NOT NULL,
    elapsed REAL NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP   
);
            """)

            self.db.commit()
            cursor.close()
        except Exception as e:
            logger.Error(f"Storage error: {e}")
            raise e

    def close(self) -> None:
        if self.db is not None:
            self.db.close()
            self.db = None  

    def insert(self, name: str, elapsed: float) -> None:
        try:
            cursor = self.db.cursor()
            
            params = (name, round(elapsed,2))
            sql = """INSERT INTO processes (name, elapsed) VALUES (?, ?);""" 

            cursor.execute(sql, params)
            cursor.close()
            
            self.db.commit()    
        except Exception as e:
            logger.Error(f"Storage error: {e}")
            raise e
        
    def get_elapsed(self) -> dict:
        ret = {}
        try:
            cursor = self.db.cursor()
            cursor.execute("""
SELECT 
    name, 
    sum(elapsed) total
FROM 
    processes 
GROUP BY
    name
ORDER BY 
    created_at desc;
            """)
            
            for row in cursor.fetchall():
                ret[row[0]] = round(row[1], 2)

            cursor.close()

        except Exception as e:
            logger.Error(f"Storage error: {e}")
            raise e
        
        return ret
        