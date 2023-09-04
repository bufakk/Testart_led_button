import sqlite3

def get_entries(db_name):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM led_event")
    entries = cursor.fetchall()

    conn.close()

    if not entries:
        print("Keine Einträge vorhanden.")
    else:
        for entry in entries:
            print(entry)

if __name__ == '__main__':
    db_name = 'button_led.db'
    get_entries(db_name)