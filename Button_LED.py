from gpiozero import LED, Button
import sqlite3
from datetime import datetime

class LEDButton:
    def init(self, led_pin, button_pin, db_name):
        self.led = LED(led_pin)
        self.button = Button(button_pin)
        self.button.when_released = self.toggle_led
        self.db_name = db_name

    def toggle_led(self):
        self.led.toggle()
        self.led_event()

    def led_event(self):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        is_on = int(self.led.is_lit)
        cursor.execute("INSERT INTO led_event (exact_time, is_on) VALUES (?, ?)", (current_time, is_on))
        conn.commit()
        conn.close()

class ORM:
    def init(self, db_name):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()

    def create_table(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS led_event (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                exact_time DATETIME NOT NULL,
                is_on BOOLEAN NOT NULL
            )
        ''')
        self.conn.commit()

    def close_connection(self):
        self.conn.close()

if __name__ == '__main__':
    db_name = 'button_led.db'
    orm = ORM(db_name)
    orm.create_table()
    led_button = LEDButton(17, 27, db_name)