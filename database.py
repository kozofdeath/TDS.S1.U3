import sqlite3 as lite;
import pandas as pd;
import random;
from city_to_state import city_to_state_dict as csd;
import os.path

warm_month_list = ['April', 'May', 'June', 'July', 'August', 'September'];
cold_month_list = ['January', 'February', 'March', 'October', 'November', 'December'];
temperature_list = range(40, 121);
year_list = range(2010, 2017);

city_list = [];
weather_list = [];

def initialize_DB():
    for city in csd:
        city_list.append((city, csd[city]));
        weather_list.append((city, random.choice(year_list), random.choice(warm_month_list), random.choice(cold_month_list), random.choice(temperature_list)));
    city_entries = tuple(city_list)
    weather_entries = tuple(weather_list)

    con = lite.connect('city_and_weather.db')
    with con:
        cur = con.cursor();
        cur.execute("CREATE TABLE weather (city text, year int, warm_month text, cold_month text, average_high int)")
        cur.execute("CREATE TABLE cities (name text, state text)");
        cur.executemany("INSERT INTO weather (city, year, warm_month, cold_month, average_high) VALUES(?,?,?,?,?)", weather_entries);
        cur.executemany("INSERT INTO cities (name, state) VALUES(?,?)", city_entries);

if not os.path.isfile('C:\Users\samko\Desktop\Programming\Thinkful\projects\U1.S3\city_and_weather.db'):
    initialize_DB();
else:
    con = lite.connect('city_and_weather.db')
    with con:
        cur = con.cursor();
        cur.execute("DELETE FROM combined WHERE 1=1;")
        cur.execute("INSERT INTO combined SELECT name, state, warm_month, average_high FROM (cities INNER JOIN weather on name=city)");
        cur.execute("SELECT * FROM combined;")
        rows = cur.fetchall();

        cur.execute("SELECT warm_month, AVG(average_high) FROM combined GROUP BY warm_month ORDER BY AVG(average_high) DESC")
        cur.execute("SELECT state, warm_month, AVG(average_high) FROM combined GROUP BY state HAVING warm_month='July'")
        cur.execute("SELECT COUNT(DISTINCT state) FROM combined WHERE warm_month ='July'");
        cur.execute("SELECT state, warm_month, AVG(average_high) FROM combined WHERE warm_month = 'July' GROUP BY state ORDER BY AVG(average_high)")

# Write a query which which finds the mean of the average high temperatures for all of the cities within a state,
# starting with the hottest, and filtering out states with a mean above 65F.

        cur.execute("SELECT state, AVG(average_high) FROM combined GROUP BY state HAVING AVG(average_high) > 80")
        rows = cur.fetchall();
        col = [desc[0] for desc in cur.description];
        output = pd.DataFrame(rows, columns = col);



print output;




# con = sqlite3.connect('database.db')
# cursor = con.cursor()
# cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
# print(cursor.fetchall())
