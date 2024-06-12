import sqlite3

DB_FILE = "../data/countries.db"

def execute_SQL_and_report(operation, success_message, failure_message, already_exists_message):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    try:
        cursor.execute(operation)
        print(f'\033[32m{success_message}\033[0m')  # Green text for success
    except sqlite3.OperationalError as e:
        if "duplicate column name" in str(e):
            print(f'\033[33m{already_exists_message}\033[0m')  # Yellow text for already exists
        else:
            print(f'\033[31m{failure_message}: {e}\033[0m')  # Red text for failure

    conn.commit()
    conn.close()

def add_columns():
    # Log the ALTER operation for adding topLevelDomain column
    execute_SQL_and_report(
        "ALTER TABLE country ADD COLUMN topLevelDomain TEXT;",
        "Successfully added 'topLevelDomain' column.",
        "Failed to add 'topLevelDomain' column.",
        "'topLevelDomain' column already exists."
    )
    
    # Log the ALTER operation for adding capital column
    execute_SQL_and_report(
        "ALTER TABLE country ADD COLUMN capital TEXT;",
        "Successfully added 'capital' column.",
        "Failed to add 'capital' column.",
        "'capital' column already exists."
    )

if __name__ == "__main__":
    add_columns()
