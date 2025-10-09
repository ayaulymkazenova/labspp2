# 1. Subtract five days from current date
from datetime import datetime, timedelta

today = datetime.now()
five_days_ago = today - timedelta(days=5)
print(five_days_ago.strftime("%Y-%m-%d"))