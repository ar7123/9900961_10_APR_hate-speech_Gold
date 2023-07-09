import sqlite3

conn = sqlite3.connect('Data - Asset Challenge/tweets.db', check_same_thread=False)

def create_database():
    conn.execute("""CREATE TABLE IF NOT EXISTS clean_tweets (id INTEGER PRIMARY KEY AUTOINCREMENT, original_tweet char(1000), cleaned_tweet char(1000))""")
    conn.commit()

def insert_to_database(value_1, value_2):
    value_1 = value_1.encode('utf-8')
    value_2 = value_2.encode('utf-8')
    query = f"INSERT INTO clean_tweets (original_tweet,cleaned_tweet) VALUES (?, ?);"
    cursors = conn.execute(query, (value_1, value_2))
    conn.commit()

def read_database(index_data=None, keywords_data=None):
    if index_data == None and keywords_data is None:
        results = conn.execute(f'select original_tweet, cleaned_tweet FROM clean_tweets;')
        results = [result for result in results]
        return results
    elif keywords_data is not None and index_data is None:
        query = f"select original_tweet, cleaned_tweet FROM clean_tweets where original_tweet like '%{keywords_data}%';"
        results = conn.execute(query)
        results = [result for result in results]
        return results
    elif keywords_data is None and index_data is not None:
        results = conn.execute(f'select original_tweet, cleaned_tweet FROM clean_tweets WHERE id = {index_data};')
        results = [result for result in results]
        return results[0]