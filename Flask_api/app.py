#
# from flask import Flask, request, jsonify
# import pandas as pd
#
# app = Flask(__name__)
#
# # Load the data
# df = pd.read_csv('Zomato_final_dockers.csv')
#
# def parse_honest_review(honest_review):
#     try:
#         review_data = eval(honest_review)
#         return {
#             'positive_reviews_count': review_data.get('positive_reviews_count'),
#             'negative_reviews_count': review_data.get('negative_reviews_count'),
#             'neutral_reviews_count': review_data.get('neutral_reviews_count')
#         }
#     except (SyntaxError, NameError):
#         return {
#             'positive_reviews_count': None,
#             'negative_reviews_count': None,
#             'neutral_reviews_count': None
#         }
# def get_filtered_data(data, df):
#     restaurant_name = data.get('restaurant_name')
#     cuisine_name = data.get('cuisine_name')
#
#
#
#     if restaurant_name:
#         result = df[df['Restaurant_name'].str.contains(restaurant_name, case=False, na=False)]
#     elif cuisine_name:
#         result = df[df['Popular_cuisines'].str.contains(cuisine_name, case=False, na=False)]
#     else:
#         return pd.DataFrame()
#
#     # Select and reorder columns
#     result = result[['Restaurant_name', 'Location', 'Average_rating', 'delivery_vs_dine_in_preference',
#                      'Popular_cuisines', 'Open_day', 'Closed_day', 'Honest_review', 'overall_review', 'Links','operational_hours']]
#
#     # Simplify the 'delivery_vs_dine_in_preference' column
#     result['delivery_vs_dine_in_preference'] = result['delivery_vs_dine_in_preference'].apply(
#         lambda x: eval(x)['preference'])
#     result['Honest_review'] = result['Honest_review'].apply(parse_honest_review)
#
#     return result
#
#
# @app.route('/get_restaurants', methods=['POST'])
# def get_restaurants():
#     data = request.get_json()
#
#     if not data:
#         return jsonify({"error": "Invalid input"}), 400
#
#     filtered_df = get_filtered_data(data, df)
#
#     if filtered_df.empty:
#         return jsonify({"error": "No matching data found"}), 404
#
#     result = filtered_df.to_dict(orient='records')
#
#     # Reorder the JSON keys
#     ordered_result = [
#         {
#             'Restaurant_name': item['Restaurant_name'],
#             'Location': item['Location'],
#             'Average_rating': item['Average_rating'],
#             'delivery_vs_dine_in_preference': item['delivery_vs_dine_in_preference'],
#             'Popular_cuisines': item['Popular_cuisines'],
#             'Open_period': f"Open from {item['Open_day']} to {item['Closed_day']}",
#             'Operational Hours ': item['operational_hours'],
#             'Honest_review': item['Honest_review'],
#             'overall_review': item['overall_review'],
#             'Links': item['Links'],
#         }
#         for item in result
#     ]
#
#     return jsonify(ordered_result)
#
#
# if __name__ == '__main__':
#     app.run(debug=True)

###############################################yoooooooooooooooooooooooooooooooooooo
# #
from flask import Flask, request, jsonify
import mysql.connector
import pandas as pd
import os
app = Flask(__name__)

def get_db_connection():
    return mysql.connector.connect(
        host=os.getenv('MYSQL_HOST', 'localhost'),
        user=os.getenv('MYSQL_USER', 'root'),
        password=os.getenv('MYSQL_PASSWORD', 'password'),
        database=os.getenv('MYSQL_DB', 'Zomato_SQL')
    )

def parse_honest_review(honest_review):
    try:
        review_data = eval(honest_review)
        return {
            'positive_reviews_count': review_data.get('positive_reviews_count'),
            'negative_reviews_count': review_data.get('negative_reviews_count'),
            'neutral_reviews_count': review_data.get('neutral_reviews_count')
        }
    except (SyntaxError, NameError):
        return {
            'positive_reviews_count': None,
            'negative_reviews_count': None,
            'neutral_reviews_count': None
        }

def get_filtered_data(data, cursor):
    restaurant_name = data.get('restaurant_name')
    cuisine_name = data.get('cuisine_name')

    query = "SELECT * FROM zomato_final_SQL_docker"
    if restaurant_name:
        query += " WHERE Restaurant_name LIKE %s"
        cursor.execute(query, ('%' + restaurant_name + '%',))
    elif cuisine_name:
        query += " WHERE Popular_cuisines LIKE %s"
        cursor.execute(query, ('%' + cuisine_name + '%',))
    else:
        return pd.DataFrame()

    result = cursor.fetchall()
    columns = [i[0] for i in cursor.description]
    df = pd.DataFrame(result, columns=columns)

    df = df[['Restaurant_name', 'Location', 'Average_rating', 'delivery_vs_dine_in_preference',
             'Popular_cuisines', 'Open_day', 'Closed_day', 'Honest_review', 'overall_review', 'Links', 'operational_hours']]

    df['delivery_vs_dine_in_preference'] = df['delivery_vs_dine_in_preference'].apply(lambda x: eval(x)['preference'])
    df['Honest_review'] = df['Honest_review'].apply(parse_honest_review)

    return df

@app.route('/get_restaurants', methods=['POST'])
def get_restaurants():
    data = request.get_json()

    if not data:
        return jsonify({"error": "Invalid input"}), 400

    conn = get_db_connection()
    cursor = conn.cursor()

    filtered_df = get_filtered_data(data, cursor)

    cursor.close()
    conn.close()

    if filtered_df.empty:
        return jsonify({"error": "No matching data found"}), 404

    result = filtered_df.to_dict(orient='records')

    ordered_result = [
        {
            'Restaurant_name': item['Restaurant_name'],
            'Location': item['Location'],
            'Average_rating': item['Average_rating'],
            'delivery_vs_dine_in_preference': item['delivery_vs_dine_in_preference'],
            'Popular_cuisines': item['Popular_cuisines'],
            'Open_period': f"Open from {item['Open_day']} to {item['Closed_day']}",
            'Operational Hours ': item['operational_hours'],
            'Honest_review': item['Honest_review'],
            'overall_review': item['overall_review'],
            'Links': item['Links'],
        }
        for item in result
    ]

    return jsonify(ordered_result)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0',port=8080)

















