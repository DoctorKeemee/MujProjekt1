import pymysql.cursors
from flask import Flask, jsonify, request

app = Flask(__name__)

db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'KarelJeL123',
    'db': 'smartwordsbo0363',
    'charset': 'utf8mb4',
    'cursorclass': pymysql.cursors.DictCursor
}


def is_integer(var):
    return isinstance(var, int)
def isRightRequest(request):
    if request.method != 'POST':
        return False, jsonify({'message': 'Invalid request method.'}), 405  # Method Not Allowed
    data = request.json

    if not data:
        return False, jsonify({'message': 'Bad request.(empty data)'}), 400  # Bad Request
    return True, data

@app.route('/createword', methods=['POST'])
def insert_word():
    cursor, connection = None, None
    check, data = isRightRequest(request)
    if not check:
        return data

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
    cursor, connection = None, None
    check, data = isRightRequest(request)
    if not check:
        return data
    if 'email' not in data:
        return jsonify({'message': "Bad request.(missing email)"}), 400 #Bad request
    email = data['email']
    if '@' not in email:
        return jsonify({'message':'Bad request.(invalid email)'}), 400 #Bad request
    split = email.split('@')
    if len(split) != 2:
        return jsonify({'message':'Bad request.(invalid email)'}), 400 #Bad request
    if "." not in split[1]:
        return jsonify({'message':'Bad request.(invalid email)'}), 400 #Bad request

    try:
        connection = pymysql.connect(**db_config)
        cursor = connection.cursor()
        sql = ("SELECT Word, Definition, Level, Explained FROM Users JOIN WordsToUsers "
               "ON Users.ID = WordsToUsers.IDUser JOIN Words ON WordsToUsers.IDWord = Words.ID "
               "WHERE Explained = 0 and Users.email = %s")
        cursor.execute(sql, email)
        connection.commit()
        words = cursor.fetchall()

        return jsonify(words), 200

    except Exception as e:
        return jsonify({'message': 'Error: ' + str(e)}), 500
    finally:
        if cursor is not None:
            cursor.close()
        if connection is not None:
            connection.close()


@app.route('/setwordlevel', methods=['POST'])
def set_word_level():
    cursor, connection = None, None
    check, data = isRightRequest(request)
    if not check:
        return data
    if "level" not in data:
        return jsonify({'message': "Bad request.(missing level)"}), 400 # Bad request
    if "word" not in data:
        return jsonify({'message': "Bad request.(missing word)"}), 400 # Bad request
    if not is_integer(data["level"]):
        return jsonify({'message': "New level must be an integer."}), 400  # Bad request
    if "explained" not in data:
        data["explained"] = 1
    if not (data["explained"] is 1 or data["explained"] is 0):
        return jsonify({'message': "Explained must be 1 or 0."}), 400 #Bad request

    try:
        connection = pymysql.connect(**db_config)
        cursor = connection.cursor()
        sql = ("SELECT * FROM Words WHERE Word = %s")
        cursor.execute(sql, data["word"])
        connection.commit()
        words = cursor.fetchall()
        #vzit id slovícka a id uzivatele a nastavit LEvel a Explained v tabulce wordstousers
        if len(words) == 0:
            return jsonify({'message': 'Word ' + data["word"] + ' does not exist.'}), 404
        sql = ("UPDATE Words SET Level = %s, Explained = %s Where  Word = %s;")
        cursor.execute(sql, (data["level"],["explained"], data["word"]) )
        if cursor.rowcount == 0:
            return jsonify({'message': 'No rows updated.'})
        else:
            return jsonify({'message': 'Update successful.'})

    except Exception as e:
        return jsonify({'message': 'Error: ' + str(e)}), 500
    finally:
        if cursor is not None:
            cursor.close()
        if connection is not None:
            connection.close()


if __name__ == '__main__':
    app.run(debug=True)
