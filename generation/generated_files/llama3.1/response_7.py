import sqlite3
from datetime import date

def connect_db(db_name):
    conn = sqlite3.connect(db_name)
    return conn

def disconnect_db(conn):
    conn.close()

def get_user_input():
    table = input("Enter the table name: ")
    filter1 = input("Enter column 1 for filtering (e.g., id, name): ")
    operator1 = input("Enter operator for filter 1 (e.g., ==, !=, >, <): ")
    value1 = input("Enter value for filter 1: ")
    filter2 = input("Enter column 2 for filtering (optional), press Enter if not needed: ")
    operator2 = input("Enter operator for filter 2 (optional), press Enter if not needed: ")
    value2 = input("Enter value for filter 2 (optional), press Enter if not needed: ")

    return table, filter1, operator1, value1, filter2, operator2, value2

def lookup_records(conn, table, filter1, operator1, value1, filter2=None, operator2=None, value2=None):
    cur = conn.cursor()
    
    query = f"SELECT * FROM {table} WHERE {filter1} {operator1} '{value1}'"
    
    if filter2 and operator2:
        query += f" AND {filter2} {operator2} '{value2}'"
        
    cur.execute(query)
    records = cur.fetchall()
    
    return records

def archive_records(conn, table, records):
    for record in records:
        delete_query = f"DELETE FROM {table} WHERE id = {record[0]}"
        conn.execute(delete_query)

def main():
    db_name = "example.db"
    conn = connect_db(db_name)
    
    table, filter1, operator1, value1, filter2, operator2, value2 = get_user_input()
    
    records = lookup_records(conn, table, filter1, operator1, value1, filter2, operator2, value2)
    
    if len(records) > 0:
        print("Records found:")
        for record in records:
            print(record)
        
        confirm = input("Do you want to archive these records? (yes/no): ")
        if confirm.lower() == "yes":
            archive_records(conn, table, records)
            
    disconnect_db(conn)

if __name__ == "__main__":
    main()