import re
import pandas as pd
import sqlite3

from flask import Flask, jsonify, request, render_template, redirect, url_for
from clean import tweet_cleaning

from flasgger import Swagger
from flasgger import swag_from

from read_and_write import create_database, insert_to_database, read_database

tweet_app = Flask(__name__, template_folder='temp')

swagger_config = {
    "headers": [],
    "specs": [{"endpoint":"docs", "route": '/docs.json'}],
    "static_url_path": "/flasgger_static",
    "swagger_ui":True,
    "specs_route":"/docs/"
}

swagger = Swagger(tweet_app,
                  config = swagger_config
                 )

TABLE_NAME = "clean_tweets"

@tweet_app.route('/', methods=['GET', "POST"])
def hello_world():
    if request.method == 'POST':
        go_to_page = request.form['inputText']
        if go_to_page == "1":
            return redirect(url_for("text_cleansing"))
        elif go_to_page == "2":
            return redirect(url_for("file_cleansing"))
        elif go_to_page == "3":
            return redirect(url_for("tweets_reading"))
    else:
        return render_template("index.html")

@tweet_app.route('/text-cleansing',methods=['GET', 'POST'])
def text_cleansing():
    if request.method == 'POST':
        original_tweet=request.form['inputText']
        cleaned_tweet=tweet_cleaning(original_tweet)
        json_response={'cleaned_tweet': cleaned_tweet,
                       'original_tweet': original_tweet
                      }
        json_response=jsonify(json_response)
        return json_response
    else:
        return render_template("text_cleansing.html")

@tweet_app.route('/file-cleansing',methods=['GET', 'POST'])
def file_cleansing():
    if request.method == 'POST':
        file = request.files['inputFile']
        df = pd.read_csv(file, encoding='latin1')
        if("Data" in df.columns):
            list_of_tweets = df['Data']
            list_of_cleaned_tweet = df['Data'].apply(lambda x: tweet_cleaning(x)) 

            create_database()
            for original_tweet, cleaned_tweet in zip(list_of_tweets, list_of_cleaned_tweet):
                insert_to_database(value_1=original_tweet, value_2=cleaned_tweet)
            
            json_response={'list_of_tweets': list_of_tweets[0],
                           'list_of_cleaned_tweet': list_of_cleaned_tweet[0]
                          }
            json_response=jsonify(json_response)
            return json_response
        else:
            json_response={'ERROR_WARNING': "Tidak ada kolom DATA, periksa kembali file Anda"}
            json_response = jsonify(json_response)
            return json_response
        return json_response
    else:
        return render_template("file_cleansing.html")

@tweet_app.route('/tweet_reading',methods=['GET', 'POST'])
def tweets_reading():
    if request.method == "POST":
        showed_index=request.form['inputIndex']
        showed_keywords = request.form['inputKeywords']
        if len(showed_index)>0:
            print("AAAAAAAAAA")
            result_from_reading_database = read_database(index_data=showed_index)
            original_tweet=result_from_reading_database[0].decode('latin1')
            cleaned_tweet=result_from_reading_database[1].decode('latin1')
            json_response={'Index': showed_index,
                           'Original_tweet': original_tweet,
                           'Cleaned_tweet': cleaned_tweet
                          }
            json_response = jsonify(json_response)
            return json_response
        elif len(showed_keywords)>0:
            print("BBBBBBBBB")
            results = read_database(keywords_data=showed_keywords)
            json_response={'showed_keywords': showed_keywords,
                           'original_tweet': results[0][0].decode('latin1'),
                           'cleaned_tweet': results[0][1].decode('latin1')
                          }
            json_response = jsonify(json_response)
            return json_response
        else:
            print("CCCCCCCC")
            json_response={'ERROR_WARNING': "INDEX OR KEYWORDS IS NONE"}
            json_response = jsonify(json_response)
            return json_response
    else:
        return render_template("tweet_reading.html")

if __name__ == '__main__':
    tweet_app.run(debug=True)