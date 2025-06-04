import sqlite3

def connect_to_database(db_name):
    return sqlite3.connect(db_name)

def lookup_records(cursor, table_name, **filters):
    query = f"SELECT * FROM {table_name}"
    if filters:
        conditions = ' AND '.join([f"{key} = ?" for key in filters])
        query += f" WHERE {conditions}"
    cursor.execute(query, tuple(filters.values()))
    return cursor.fetchall()

def archive_records(cursor, table_name, archive_table, **filters):
    records = lookup_records(cursor, table_name, **filters)
    if records:
        insert_query = f"INSERT INTO {archive_table} SELECT * FROM {table_name} WHERE "
        conditions = ' AND '.join([f"{key} = ?" for key in filters])
        delete_query = f"DELETE FROM {table_name} WHERE {conditions}"
        cursor.execute(insert_query + conditions, tuple(filters.values()))
        cursor.execute(delete_query, tuple(filters.values()))

def main():
    db_name = input("Enter the database name: ")
    table_name = input("Enter the table name to look up records from: ")
    archive_table = input("Enter the archive table name: ")
    filter_key = input("Enter the filter key (column name): ")
    filter_value = input("Enter the filter value: ")

    conn = connect_to_database(db_name)
    cursor = conn.cursor()

    print("\nRecords found:")
    records = lookup_records(cursor, table_name, **{filter_key: filter_value})
    for record in records:
        print(record)

    confirm = input(f"\nArchive these {len(records)} records? (yes/no): ")
    if confirm.lower() == 'yes':
        archive_records(cursor, table_name, archive_table, **{filter_key: filter_value})
        conn.commit()
        print("Records archived successfully.")
    else:
        print("No records were archived.")

    cursor.close()
    conn.close()

if __name__ == "__main__":
    main()