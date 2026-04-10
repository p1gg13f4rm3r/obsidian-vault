import sqlite3
from datetime import datetime, timedelta

conn = sqlite3.connect('data/trading.db')
cursor = conn.cursor()

# Get META data from daily_prices
cursor.execute("SELECT * FROM daily_prices WHERE symbol = 'META' ORDER BY date DESC LIMIT 5;")
rows = cursor.fetchall()
print('META recent rows:')
for row in rows:
    print(row)

# Get column names
cursor.execute("PRAGMA table_info(daily_prices);")
cols = cursor.fetchall()
print('\ndaily_prices columns:', cols)

# Check latest date freshness
cursor.execute("SELECT date, close FROM daily_prices WHERE symbol = 'META' ORDER BY date DESC LIMIT 1;")
latest = cursor.fetchone()
print('\nLatest META:', latest)
if latest:
    latest_date = datetime.fromisoformat(latest[0])
    now = datetime.now()
    age_minutes = (now - latest_date).total_seconds() / 60
    print('Age (minutes):', age_minutes)
    print('Is fresh (within 20 min):', age_minutes < 20)

conn.close()
