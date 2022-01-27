from flask import Flask, request, make_response, redirect, render_template, send_from_directory
from werkzeug.utils import html
import pandas as pd

app = Flask(__name__, static_folder="static")

df = pd.read_csv('DB.csv')
data_extract = range(len(df))
summoners_datas = []
summoners_data_first_line = []
columns_names = [
'Streamer',
'Nombre de Invocador',
'División',
'Puntos de Liga',
'Partidas Jugadas',
'Victorias',
'Derrotas',
'Win Ratio %']
summoner_data_first_line = (df.iloc[:, 0])
summoners_data_first_line.append(summoner_data_first_line.values)
# print(summoners_data_first_line)

for data in data_extract:
    summoner_data = (df.iloc[data,0:8])
    summoners_datas.append(summoner_data.values)
print(summoners_datas)

summoners_data_table = zip(summoners_data_first_line, summoners_datas)
@app.route('/')
def index():
    user_ip = request.remote_addr
    
    response = make_response(redirect('/hello'))
    response.set_cookie('user_ip', user_ip)

    return response

@app.route('/hello')

def hello():
    user_ip = request.cookies.get('user_ip')
    context = {
        'user_ip' : user_ip,
        'data_extract' : data,
        'columns_names' : columns_names,
        'summoners_datas' : summoners_datas,
    }
    return render_template('hello.html', **context)

@app.route('/riot.txt')
def static_from_root():
    return send_from_directory(app.static_folder, request.path[1:])