import config
import sqlite3
import datetime


def get_label():
    # we don't handle exceptions, because the system exceptions tell everything what's needed if something goes wrong
    conn = sqlite3.connect(config.db_path)
    c = conn.cursor()
    c.execute('SELECT activity_id, start_time, end_time, name FROM facts \
        LEFT  JOIN activities on facts.activity_id = activities.id \
        ORDER BY start_time DESC \
        LIMIT 1')
    row = c.fetchone()
    if row is None:
        raise Exception('Handling of completely empty rows isn\'t implemented yet')
    if row[2] is None:
        begin = datetime.datetime.strptime(row[1], "%Y-%m-%d %H:%M:%S")
        now = datetime.datetime.now()
        duration = str(now - begin)
        pos = duration.find('.')
        seconds = duration[:pos]
        activity = row[3]
        labeltext = activity + ' ' + seconds
    else:
        labeltext = 'No Activity'
    conn.close()
    return labeltext
