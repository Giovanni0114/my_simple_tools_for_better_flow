import sqlite3

conn = sqlite3.connect('words.sqlite')

c = conn.cursor()
c.execute('CREATE TABLE words (word VARCHAR)')

with open("/usr/share/dict/words") as file:
    for line in file.readlines():
        c.execute(f'INSERT INTO words VALUES ("{line.rstrip().upper()}")')

conn.commit()
conn.close()