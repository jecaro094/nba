# imports

import os

import urllib.parse as urlparse
import pandas as pd
import matplotlib.pyplot as plt

from urllib.parse import parse_qs
from random import randint
from flask import Flask, render_template, request, redirect

# functions

def get_sort(sort):
    """
    Consider ascending/descending
    """
    if sort=="Ascending":
        return True
    elif sort=="Descending":
        return False

def get_bool_from_drop(drop):
    """
    Consider (or not) zero values in DF
    """
    if drop=="Remove zeros":
        return True
    elif drop=="Do not remove zeros":
        return False

def get_df_stat(text_stat):
    """
    Returns the stat name for the DF
    """
    stat = text_stat.split()[0]
    if stat!="Minutes":
        return f"{stat}PG"
    else:
        return "MPG"
    
async def generate_graph_image(stat, sort, limit, drop_zeros):
    """
    Generate graph from the DF and parameters
    """
    stat_selected = get_df_stat(stat) 
    df_nba_ = df_nba.copy()
    
    # NOTE Exclude zero values from a copy of the original DF, for the stat considered
    if get_bool_from_drop(drop_zeros):
        indexes = df_nba_.index[df_nba_[stat_selected]==0].to_list()
        df_nba_ = df_nba_.drop(indexes)

    # NOTE Get the figure, considering the parameters of this function
    df_sorted = df_nba_.sort_values(stat_selected, ascending=get_sort(sort))[:int(limit)]
    ax = df_sorted.plot.bar(x='FULL NAME', y=stat_selected, rot=90, color="#8ad900", figsize=(6, 6))

    # NOTE Saved graph figure in "figure_path" folder
    plt.savefig(figure_path, bbox_inches='tight')

    # NOTE Close open figure
    plt.close('all')

    
def get_param(url, param):
    """
    Returns the value of the specified parameter
    from a URL string
    """
    parsed = urlparse.urlparse(url)
    return (parse_qs(parsed.query)[param])[0]

def get_params(url):
    """
    Returns all parameters from URL at once
    """
  
    return [get_param(url, "statics"), get_param(url, "limit"), \
            get_param(url, "arrange"), get_param(url, "drop")]

def get_options(default_options=False):
    """
    Returns options to be displayed in the HTML
    """
    if default_options:
        return [stats[0], lim[0], arrange[0], drop[0]]
    else:
        return [stats, lim, arrange, drop]

# NOTE Define a DF and options to be displayed in HTML page

csv_path = os.path.join(os.getcwd(), "NBA2021.csv")
figure_path = os.path.join(os.getcwd(), "static", 'saved_figure.png')
with open(csv_path, "r") as csv_file:
    df_nba = pd.read_csv(csv_file)

drop = ["Remove zeros", "Do not remove zeros"]
stats = ["Points per Game", "Assists per Game", "Rebounds per Game", \
        "Steals per Game", "Minutes per Game"]
lim = ["5","10","15","20","25"]
arrange= ["Ascending", "Descending"]

# NOTE Defining the app

app = Flask(__name__)

@app.route('/')
def hello_world():
    return redirect("/nbastats")

@app.route('/nbastats', methods=['GET'])
async def stats_function():

    try:
        [stat, lim, arr, drp] = get_params(request.url)
    except:
        [stat, lim, arr, drp] = get_options(default_options=True)

    await generate_graph_image(stat, arr, lim, drp)
    return render_template('page.html', options_=get_options(), arr = arr, lim=lim, stat=stat, drp=drp)

if __name__ == '__main__':
    app.run()   

