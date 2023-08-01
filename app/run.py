import json
import plotly
import pandas as pd
import joblib

from flask import Flask, render_template, request, jsonify
from plotly.graph_objs import Bar

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
    # TODO: Below is an example - modify to extract data for your own visuals
    genre_counts = df_message.groupby('genre').count()['message']
    genre_names = list(genre_counts.index)
    
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
        }
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
    # render pandas df on html
    results = df_message[:25].to_dict('records')
    return render_template('table.html', results=results, titles=['message', 'genre'])

@app.route('/get-next-rows')
def get_next_rows():
    offset = int(request.args['offset']) if 'offset' in request.args else 0
    results = df_message[offset:offset+25].to_dict('records')
    return render_template('table_rows.html', results=results, offset=offset+25)

def main():
    app.run(host='0.0.0.0', port=3001, debug=True)


if __name__ == '__main__':
    main()