import time  
import psycopg2
from datetime import datetime, timedelta, timezone
import re
from api_request import fetcha_data

def connect_to_db():
    print("Connecting to the database...")
    try:
        conn = psycopg2.connect(
            host="db",
            port="5432",
            dbname="db",
            user="db_user",
            password="db_password"
        )
        return conn
    except psycopg2.Error as e:
        print("Connection failed:")
        print(f"  pgcode={getattr(e, 'pgcode', None)}")
        print(f"  pgerror={getattr(e, 'pgerror', None)}")
        print(f"  diag={getattr(e, 'diag', None)}")
        return None

def wait_for_db(max_tries=15, delay=1.0):
    for i in range(max_tries):
        conn = connect_to_db()
        if conn:
            try:
                with conn.cursor() as cur:
                    cur.execute("SELECT 1")
                print("Database is ready.")
                return conn
            except psycopg2.Error:
                pass
        print(f"DB not ready yet ({i+1}/{max_tries})...")
        time.sleep(delay)
    raise RuntimeError("Database did not become ready in time.")


def create_table(conn):
    print("Creating table if it does not exist...")
    try:
        with conn.cursor() as cursor:
            cursor.execute("""
                CREATE SCHEMA IF NOT EXISTS dev;
                CREATE TABLE IF NOT EXISTS dev.raw_weather_data(
                    id SERIAL PRIMARY KEY,
                    city TEXT,
                    temperature FLOAT,
                    weather_description TEXT,
                    wind_speed FLOAT,
                    time TIMESTAMP,
                    inserted_at TIMESTAMP DEFAULT NOW(),
                    utc_offset TEXT
                );
            """)
        conn.commit()
        print("Table created successfully.")
    except psycopg2.Error as e:
        print(f"An error occurred while creating the table: {e}")
        raise


import re

def _parse_obs_timestamp(observation_time: str, utc_offset: str) -> datetime:
    """
    observation_time: e.g. "07:40 AM"
    utc_offset: accepts "+05:00", "-0400", "+5", "-5.5", "UTC+5:30", "4.", "+4.75", etc.
    Returns a naive UTC datetime suitable for a TIMESTAMP column.
    """
    # 1) parse the clock time
    t = datetime.strptime(observation_time.strip(), "%I:%M %p").time()

    # 2) robustly parse the UTC offset
    off = utc_offset.strip().upper()

    # strip leading "UTC"
    if off.startswith("UTC"):
        off = off[3:].strip()

    # default sign if missing: assume '+'
    sign = 1
    if off.startswith(("+", "-")):
        sign = 1 if off[0] == "+" else -1
        off_body = off[1:]
    else:
        off_body = off

    off_body = off_body.replace(" ", "")

    hours = 0
    minutes = 0

    # case A: HH:MM or HHMM
    m = re.fullmatch(r"(\d{1,2}):?(\d{2})", off_body)
    if m:
        hours = int(m.group(1))
        minutes = int(m.group(2))
    else:
        # case B: decimal hours like "5", "5.", "5.5", "5.75", "5.25"
        # if it’s something like "4." float() handles it (becomes 4.0)
        try:
            val = float(off_body)
            hours = int(abs(val))
            minutes = int(round((abs(val) - hours) * 60))
        except ValueError:
            raise ValueError(f"Unrecognized utc_offset format: {utc_offset!r}")

    delta = timedelta(hours=hours, minutes=minutes) * sign
    tz = timezone(delta)

    # 3) assume the observation date is "today" in that location
    local_today = datetime.now(tz).date()
    local_dt = datetime.combine(local_today, t, tzinfo=tz)

    # 4) convert to UTC and drop tzinfo for a TIMESTAMP column (naive UTC)
    return local_dt.astimezone(timezone.utc).replace(tzinfo=None)

def insert_records(conn, data):
    print("Inserting records into the database...")
    try:
        weather = data['current']
        location = data['location']

        # Prefer a ready-made local datetime if your API provides it (e.g. Weatherstack 'localtime': "2024-08-19 07:40")
        # Otherwise, build it from observation_time + utc_offset:
        obs_ts = _parse_obs_timestamp(weather['observation_time'], location['utc_offset'])

        with conn.cursor() as cursor:
            cursor.execute("""
                INSERT INTO dev.raw_weather_data (
                    city,
                    temperature,
                    weather_description,
                    wind_speed,
                    time,
                    inserted_at,
                    utc_offset
                ) VALUES (%s, %s, %s, %s, %s, NOW(), %s)
            """, (
                location['name'],
                weather['temperature'],
                weather['weather_descriptions'][0],
                weather['wind_speed'],
                obs_ts,                      # <-- full timestamp now
                location['utc_offset']
            ))
        conn.commit()
        print("Data successfully inserted into the database")
    except psycopg2.Error as e:
        print(f"An error occurred while inserting data: {e}")
        raise


def main():
    conn = None
    try:
        conn = wait_for_db()
        create_table(conn)
        data = fetcha_data()
        insert_records(conn, data)
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        if conn:
            conn.close()
            print("Database connection closed.")



