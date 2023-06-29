import pandas as pd
from flask import Flask, jsonify
import psycopg2
import pandas as pd

app = Flask(__name__)

conn = psycopg2.connect(database="lab14", user="postgres", password="1234", host = "localhost", port = 5432)

path = "dataset.csv"
datos = pd.read_csv(path)
@app.route('/covid/insert', methods=['POST'])
def insert_data():
    try:
        cursor = conn.cursor()
        query = "INSERT INTO covid_vaccination_vs_mortality (id,country,iso_code,date,total_vaccinations,people_vaccinated,people_fully_vaccinated,new_deaths,population,ratio) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        for _, row in datos.iterrows():
            print(row['country'])
            cursor.execute(query, (
                row['id'], 
                row['country'], 
                row['iso_code'], 
                row['date'], 
                row['total_vaccinations'], 
                row['people_vaccinated'],
                row['people_fully_vaccinated'], 
                row['New_deaths'],
                row['population'],
                row['ratio'] 
                ))
        
        conn.commit()
      
        return jsonify('Data inserted successfully!')
    except Exception as e:
        return str(e)

@app.route('/covid/report/country/<string:country>')
def get_report_by_country(country):
    try:
        cursor = conn.cursor()
        cursor.execute('''
            SELECT total_vaccinations, new_deaths, date
            FROM COVID_vaccination_vs_mortality
            WHERE country = %s
            ORDER BY date ASC
        ''', (country,))

        data = cursor.fetchall()
        
        return jsonify(data)
    except Exception as e:
        return str(e)

@app.route('/covid/report/year/<int:year>')
def get_report_by_year(year):
    try:
        cursor = conn.cursor()
        cursor.execute('''
            SELECT total_vaccinations, new_deaths, date
            FROM COVID_vaccination_vs_mortality
            WHERE EXTRACT(YEAR FROM date) = %s
            ORDER BY date ASC
        ''', (year,))

        data = cursor.fetchall()
        return jsonify(data)
    except Exception as e:
        return str(e)
    
if __name__ == '__main__':
    app.run()