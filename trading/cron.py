from datetime import datetime

from stock.management.commands.populate_default_data import Command

def refresh_data():
    print("CRON trigerred at: {} !".format(datetime.now()))
    Command().refresh_data()
    print("CRON completed at: {} !".format(datetime.now()))