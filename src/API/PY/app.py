from flask import Flask, request, jsonify
import pymysql.cursors

app = Flask(__name__)

db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'KarelJeL123',
    'db': 'smartwordsbo0363',
    'charset': 'utf8mb4',
    'cursorclass': pymysql.cursors.DictCursor
}


@app.route('/createword', methods=['POST'])
def insert_word():
    if request.method != 'POST':
        return jsonify({'message': 'Invalid request method.'}), 405  # Method Not Allowed
    data = request.json

    if not data:
        return jsonify({'message': 'Bad request.(empty data)'}), 400  # Bad Request

    if 'word' not in data:
        return jsonify({'message': 'Bad request.(missing word)'}), 400  # Bad Request

    if 'definition' not in data:
        return jsonify({'message': 'Bad request.(missing definition)'}), 400  # Bad Request
    word = data['word']
    definition = data['definition']

    try:

        connection = pymysql.connect(**db_config)
        cursor = connection.cursor()
        sql = "INSERT INTO Words (word, definition) VALUES (%s, %s)"
        cursor.execute(sql, (word, definition))
        connection.commit()
        return jsonify({'message': 'Insert successful'}), 200

    except Exception as e:
        return jsonify({'message': 'Error: ' + str(e)}), 500
    finally:
        if cursor is not None:
            cursor.close()
        if connection is not None:
            connection.close()

@app.route('/getword', methods=['POST'])
def get_word():
    if request.method != 'POST':
        return jsonify()



if __name__ == '__main__':
    app.run(debug=True)
