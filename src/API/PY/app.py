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

def is_valid_email_in_data(data, check):
    if not check:
        return check, data
    if 'email' not in data:
        return False, jsonify({'message': "Bad request.(missing email)"}), 400 #Bad request
    email = data['email']
    if '@' not in email:
        return False,jsonify({'message':'Bad request.(invalid email)'}), 400 #Bad request
    split = email.split('@')
    if len(split) != 2:
        return False, jsonify({'message':'Bad request.(invalid email)'}), 400 #Bad request
    if "." not in split[1]:
        return False, jsonify({'message':'Bad request.(invalid email)'}), 400 #Bad request
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
    check, data = is_valid_email_in_data(data, check)
    if not check:
        return data

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
    check, data = is_valid_email_in_data(data, check)
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
    if not (data["explained"] == 1 or data["explained"] == 0):
        return jsonify({'message': "Explained must be 1 or 0."}), 400 #Bad request

    try:
        connection = pymysql.connect(**db_config)
        cursor = connection.cursor()
        sql = ("SELECT * FROM Words WHERE Word = %s")
        cursor.execute(sql, data["word"])
        connection.commit()
        words = cursor.fetchall()

        sql = ("SELECT * FROM users WHERE Email = %s")
        cursor.execute(sql, data['email'])
        connection.commit()
        users = cursor.fetchall()

        if len(words) == 0:
            return jsonify({'message': 'Word ' + data["word"] + ' does not exist.'}), 404
        if len(users) == 0:
            return jsonify({'message': 'User ' + data["email"] + ' does not exist.'}), 404

        sql = ("SELECT * FROM wordstousers Where  IDWord = %s and IDUser = %s;")
        cursor.execute(sql, (words[0]["ID"],users[0]['ID'] ) )
        connection.commit()
        wordstousers = cursor.fetchall()

        if len(wordstousers) == 0:
            #insert
            sql = ("INSERT INTO wordstousers (Level, Explained, IDWord, IDUser) VALUES (%s, %s, %s, %s)")
            cursor.execute(sql, (data["level"], data["explained"], words[0]["ID"], users[0]['ID']))
            connection.commit()
            if cursor.rowcount == 0:
                return jsonify({'message': 'Insert failed.'}), 409
            else:
                return jsonify({'message': 'Insert successful.'}), 200
        else:
            #update
            sql = ("UPDATE wordstousers SET Level = %s, Explained = %s Where  IDWord = %s and IDUser = %s;")
            cursor.execute(sql, (data["level"],data["explained"], words[0]["ID"],users[0]['ID'] ) )
            connection.commit()
            if cursor.rowcount == 0:
                return jsonify({'message': 'No rows updated.'}), 202
            else:
                return jsonify({'message': 'Update successful.'}), 200

    except Exception as e:
        return jsonify({'message': 'Error: ' + str(e)}), 500
    finally:
        if cursor is not None:
            cursor.close()
        if connection is not None:
            connection.close()


if __name__ == '__main__':
    app.run(debug=True)
