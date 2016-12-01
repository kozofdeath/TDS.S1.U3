# The sqlite3 module is used to work with the SQLite database.
import sqlite3 as lite
import pandas as pd

# Here you connect to the database. The `connect()` method returns a connection object.
con = lite.connect('getting_started.db')

weather = (('Las Vegas', 2013, 'July', 'December', 62), ('Atlanta', 2013, 'July', 'January', 62), ('Albany', 2013, 'July', 'October', 205), ('Springfield', 2013, 'August', 'Faguary', 99), ('Dongsberg', 2013, 'June', 'Faguary', 115));
cities = (('Las Vegas', 'Nevada'), ('Atlanta', 'Georgia'), ('Springfield', 'Illinois'), ('Albany', 'NY'));
print cities;

with con:
  # From the connection, you get a cursor object. The cursor is what goes over the records that result from a query.
  cur = con.cursor()
  cur.execute('SELECT SQLITE_VERSION()')
  # You're fetching the data from the cursor object. Because you're only fetching one record, you'll use the `fetchone()` method.
  #If fetching more than one record, use the `fetchall()` method.
  data = cur.fetchone()
  # Finally, print the result.
  print("SQLite version: %s" % data);

  cur.executemany("INSERT INTO cities VALUES (?,?)", cities);
  cur.executemany("INSERT INTO weather VALUES (?,?,?,?,?)", weather);

  cur = con.cursor()
  cur.execute("SELECT * FROM weather")
  rows = cur.fetchall()
  for row in rows:
    print row;

  cols = [desc[0] for desc in cur.description]
  df = pd.DataFrame(rows, columns=cols);

  print df;

  cur.execute("""SELECT state, AVG(average_high) FROM (
    SELECT name, state, year, warm_month, average_high FROM weather INNER JOIN cities ON name = city)
    GROUP BY state;""")
  cols = [desc[0] for desc in cur.description];
  rows = cur.fetchall()
  df = pd.DataFrame(rows, columns=cols)

  print df;

  cur.execute("INSERT INTO TABLE city_state_weather SELECT warm_month, average_high FROM weather GROUP BY warm_month");
  cur.execute("SELECT * FROM city_state_weather");
  rows = cur.fetchall();
  df = pd.DataFrame(rows)

  print df;

c = [(el[0], el[1]) for el in weather];
print c;
