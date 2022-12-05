import sqlite3

def sc_create_table(sc_cursor):
    sc_cursor.execute(
        'CREATE TABLE IF NOT EXISTS serverchat(dates TEXT PRIMARY KEY, msgs INTEGER, chars INTEGER, links INTEGER, files)'
    )


def sc_data_entry(sc_cursor, sc_DB, dates, msgs, chars, links, files):
    sc_cursor.execute(
		'INSERT OR IGNORE INTO serverchat VALUES(?, ?, ?, ?, ?)',
                      (dates, msgs, chars, links, files))
    sc_DB.commit()


def sc_get_data(sc_cursor):
    sc_cursor.execute(
		'SELECT * from serverchat'
	)
    data = sc_cursor.fetchall()
    for d in data:
        print(d)


def sc_update(sc_cursor, sc_DB, msgs, chars, links, files, dates):
    sc_cursor.execute(
        'UPDATE serverchat SET msgs = msgs + {}, chars = chars + {}, links = links +{}, files = files + {} WHERE dates = "{}"'
		.format(msgs, chars, links, files, dates)
	)
    sc_DB.commit()


def uc_create_table(uc_cursor, dates):
    uc_cursor.execute(
        'CREATE TABLE IF NOT EXISTS {}(ID TEXT PRIMARY KEY, msgs INTEGER, chars INTEGER)'
        .format(dates))


def uc_data_entry(uc_cursor, uc_DB, dates, user):
    uc_cursor.execute(
		'INSERT OR IGNORE INTO {} VALUES(?, ?, ?)'
		.format(dates),
		(user, 0, 0)
	)
    uc_DB.commit()


def uc_update(uc_cursor, uc_DB, user, msgs, chars, dates):
    uc_cursor.execute(
        'UPDATE {} SET msgs = msgs + {}, chars = chars + {} WHERE ID = "{}"'.
        format(dates, msgs, chars, user))
    uc_DB.commit()
