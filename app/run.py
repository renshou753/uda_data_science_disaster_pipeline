import json
import plotly
import pandas as pd
import joblib

from flask import Flask, render_template, request, jsonify
from plotly.graph_objs import Bar, Pie
from pandas_profiling import ProfileReport

from extensions import engine
from utility import tokenize

app = Flask(__name__)

# load data
df_message = pd.read_sql_table('Message', engine)

# load model
model_message = joblib.load("../models/classifier.pkl")

# index webpage displays cool visuals and receives user input text for model
@app.route('/')
@app.route('/index')
def index():
    
    # extract data needed for visuals
    genre_counts = df_message.groupby('genre').count()['message']
    genre_names = list(genre_counts.index)

    category_names = df_message.iloc[:, 4:].columns
    category_counts = (df_message.iloc[:, 4:]!=0).sum()

    df_news = df_message[df_message['genre'] == 'news']
    news_category_names = df_news.iloc[:, 4:].columns
    news_category_counts = (df_news.iloc[:, 4:]!=0).sum()

    # create visuals
    # TODO: Below is an example - modify to create your own visuals
    graphs = [
        {
            'data': [
                Bar(
                    x=genre_names,
                    y=genre_counts
                )
            ],

            'layout': {
                'title': 'Distribution of Message Genres',
                'yaxis': {
                    'title': "Count"
                },
                'xaxis': {
                    'title': "Genre"
                }
            }
        },

        {
            'data': [
                Pie(
                    labels=category_names,
                    values=category_counts
                )
            ],

            'layout': {
                'title': 'Distribution of Categories',
                'yaxis': {
                    'title': "Count"
                },
                'xaxis': {
                    'title': "Category"
                }
            }
        },

        {
            'data': [
                Bar(
                    x=news_category_names,
                    y=news_category_counts
                )
            ],

            'layout': {
                'title': 'Distribution of News Categories',
                'yaxis': {
                    'title': "News Category Count"
                },
                'xaxis': {
                    'title': "Category"
                }
            }
        },
    ]
    
    # encode plotly graphs in JSON
    ids = ["graph-{}".format(i) for i, _ in enumerate(graphs)]
    graphJSON = json.dumps(graphs, cls=plotly.utils.PlotlyJSONEncoder)
    
    # render web page with plotly graphs
    return render_template('home.html', ids=ids, graphJSON=graphJSON)


# web page that handles user query and displays model results
@app.route('/go')
def go():
    # save user input in query
    query = request.args.get('query', '') 

    # use model to predict classification for query
    classification_labels = model_message.predict([query])[0]
    classification_results = dict(zip(df_message.columns[4:], classification_labels))

    # This will render the go.html Please see that file. 
    return render_template(
        'go.html',
        query=query,
        classification_result=classification_results
    )

# web page that render the raw table data from db
@app.route('/table')
def display_table():
    # render pandas df on dict records
    results = df_message[:25].to_dict('records')
    return render_template('table.html', results=results, titles=['message', 'genre'])

# web page that search the raw table data from db
@app.route('/search_table')
def search_table():
    # save user input in query
    query = request.args.get('query', '') 
    df = df_message[df_message.message.str.contains('{}'.format(query))]
    # render pandas to dict records
    results = df[:25].to_dict('records')
    return render_template('search_table.html', results=results, titles=['message', 'genre'], search_msg=query)

@app.route('/get-next-rows')
def get_next_rows():
    offset = int(request.args['offset']) if 'offset' in request.args else 0
    search_msg = request.args['search_msg'] if 'search_msg' in request.args else ''
    if len(search_msg) > 0:
        df = df_message[df_message.message.str.contains('{}'.format(search_msg))][offset:offset+25]
    else:
        df = df_message[offset:offset+25]
    results = df.to_dict('records')
    return render_template('table_rows.html', results=results, offset=offset+25, search_msg=search_msg)

@app.route('/profiling')
def profiling():
    return render_template('profiling.html')

def main():
    app.run(host='0.0.0.0', port=3001, debug=True)


if __name__ == '__main__':
    main()