import psycopg2
# import pdb
from os import getenv
from dotenv import load_dotenv
from pathlib import Path
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from datetime import datetime

load_dotenv(verbose=True)


def connect():
    con = psycopg2.connect(f'user={getenv("POSTGRESS_USER")} password={getenv("POSTGRES_PASS")}')
    return con

def disconnect(con):
    if con is not None:
        con.close()

def create_database():
    try:
        con = connect()
        con.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cursor = con.cursor()
        name_Database   = "discordbot"
        sqlCreateDatabase = "create database "+name_Database+";"
        cursor.execute(sqlCreateDatabase)
        cursor.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        disconnect(con)    

def create_table(commands):
    con = None
    try:
        con = connect()
        cursor = con.cursor()
        for command in commands:
            cursor.execute(command)
        cursor.close()
        con.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        disconnect(con)

def create_table_bingo_words():
    commands = (
        """
        CREATE TABLE wordbingo (
            bingo_word VARCHAR(225) PRIMARY KEY,
            bingo_scored BOOL NOT NULL,
            bingo_stamp DATE
        )
        """,
        )
    create_table(commands)

def insert_bingo_words(word):
    sql = "INSERT INTO wordbingo(bingo_word, bingo_scored, bingo_stamp) VALUES(%s, %s, %s);"
    command = (word, False, datetime.today().strftime('%Y-%m-%d'))
    con = None
    try:
        con = connect()
        cursor = con.cursor()
        cursor.execute(sql, command)
        cursor.close()
        con.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        disconnect(con)

def get_bingo_words():
    con = None
    try:
        con = connect()
        cursor = con.cursor()
        cursor.execute("SELECT bingo_word, bingo_scored, bingo_stamp FROM wordbingo")
        words = cursor.fetchall()
        cursor.close()
        return words
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        disconnect(con)

def get_bingo_result(word):
    con = None
    try:
        con = connect()
        cursor = con.cursor()
        cursor.execute("SELECT bingo_word, bingo_scored, bingo_stamp FROM wordbingo WHERE bingo_word = %s", (word,))
        words = cursor.fetchone()
        cursor.close()
        return words
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        disconnect(con)

def update_bingo_words(bingo_word, bingo_scored):
    sql = """ UPDATE wordbingo
                SET bingo_scored = %s, bingo_stamp = %s
                WHERE bingo_word = %s"""
    command = (bingo_scored, datetime.today().strftime('%Y-%m-%d'), bingo_word)
    con = None
    try:
        con = connect()
        cursor = con.cursor()
        cursor.execute(sql, (command))
        con.commit()
        cursor.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if con is not None:
            con.close()

def reset_bingo_words():
    sql = """ UPDATE wordbingo
                SET bingo_scored = False
                WHERE bingo_scored = True"""
    con = None
    try:
        con = connect()
        cursor = con.cursor()
        cursor.execute(sql)
        con.commit()
        cursor.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if con is not None:
            con.close()

def count_bingo_words(state):
    sql = """ SELECT COUNT(*) FROM wordbingo WHERE bingo_scored = %s"""
    con = None
    try:
        con = connect()
        cursor = con.cursor()
        cursor.execute(sql, (state,))
        con.commit()
        count = int(cursor.fetchone()[0])
        cursor.close()
        return count
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if con is not None:
            con.close()

def count_all_bingo_words():
    sql = """ SELECT COUNT(*) FROM wordbingo"""
    con = None
    try:
        con = connect()
        cursor = con.cursor()
        cursor.execute(sql)
        con.commit()
        count = int(cursor.fetchone()[0])
        cursor.close()
        return count
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if con is not None:
            con.close()

if __name__ == '__main__':
    create_database()
    create_table_bingo_words()


