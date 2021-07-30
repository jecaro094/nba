# imports
import pandas as pd
import matplotlib.pyplot as plt
import os

import random # remove

from flask import Flask, render_template, request

# functions

def get_sort(sort):
    if sort=="Ascending":
        return True
    elif sort=="Descending":
        return False

def get_df_stat(text_stat):
    """
    Returns the column name used in the dataframe,
    considering the text for the stat
    """
    stat = text_stat.split()[0]
    if stat!="Minutes":
        return f"{stat}PG"
    else:
        return "MPG"
    
async def generate_graph_image(stat, sort, limit):
    stat_selected = get_df_stat(stat) 
    df_sorted = df_nba.sort_values(stat_selected, ascending=get_sort(sort))[:int(limit)]
    ax = df_sorted.plot.bar(x='FULL NAME', y=stat_selected, rot=90)
    # not to show graph

    # Saved in the same folder
    plt.savefig(figure_path, bbox_inches='tight')
    
def get_param(url, param):
    import urllib.parse as urlparse
    from urllib.parse import parse_qs
    parsed = urlparse.urlparse(url)
    return (parse_qs(parsed.query)[param])[0]

def get_options():
    return [stats, lim, arrange]

csv_path = os.path.join(os.getcwd(), "NBA2021.csv")
figure_path = os.path.join(os.getcwd(),"..", "static", 'saved_figure.png')
with open(csv_path, "r") as csv_file:
    df_nba = pd.read_csv(csv_file)

stats = ["Points per Game", "Assists per Game", "Rebounds per Game", \
        "Steals per Game", "Minutes per Game"]
lim = ["5","10","15","20","25"]
arrange= ["Ascending", "Descending"]


app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
async def hello_world():

    url = request.url
    [stat, lim, arr] = get_options()

    await generate_graph_image(stat[0], arr[0], lim[0])
    return render_template('page.html', options_=get_options(), arr=arr[0], lim=lim[0], stat=stat[0])

@app.route('/nbastats', methods=['GET', 'POST'])
async def stats_function():

    stat = get_param(request.url, "statics")
    lim = get_param(request.url, "limit")
    arr = get_param(request.url, "arrange")

    await generate_graph_image(stat, arr, lim)
    return render_template('page.html', options_=get_options(), arr = arr, lim=lim, stat=stat)

if __name__ == '__main__':
    app.run()   

# export FLASK_APP=app.py
# python -m flask run