"""
import json
from pynamodb.models import Model
from pynamodb.attributes import UnicodeAttribute
from pynamodb.exceptions import PutError, DoesNotExist

# Definizione del modello User
class User(Model):
    class Meta:
        table_name = 'NomeDellaTuaTabellaUser'
        region = 'us-east-1'

    user_id = UnicodeAttribute(hash_key=True)
    name = UnicodeAttribute()
    email = UnicodeAttribute()

# Funzione per creare un nuovo utente
def createUser(event, context):
    try:
        # Ottenere i dati dell'utente dal corpo della richiesta
        user_data = json.loads(event['body'])

        # Creare un nuovo utente utilizzando i dati ricevuti
        user = User(
            user_id=user_data['user_id'],
            name=user_data['name'],
            email=user_data['email']
        )
        user.save()

        # Costruisci la risposta
        response = {
            'statusCode': 200,
            'body': json.dumps({'message': 'User created successfully'})
        }
    except KeyError:
        # Se i dati dell'utente non sono completi, restituisci un messaggio di errore
        response = {
            'statusCode': 400,
            'body': json.dumps({'error': 'Missing required user data'})
        }
    except PutError as e:
        # Se si verifica un errore durante il salvataggio dell'utente, restituisci un messaggio di errore
        response = {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }
    except Exception as e:
        # Gestisci altri errori
        response = {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }

    return response

# Funzione per ottenere un utente per ID
def getUserById(event, context):
    try:
        # Ottieni l'ID dell'utente dalla richiesta
        user_id = event['pathParameters']['user_id']

        # Cerca l'utente nella tabella DynamoDB utilizzando PynamoDB
        user = User.get(user_id)

        # Costruisci la risposta
        response = {
            'statusCode': 200,
            'body': json.dumps({
                'user_id': user.user_id,
                'name': user.name,
                'email': user.email
            })
        }
    except DoesNotExist:
        # Se l'utente non esiste, restituisci un messaggio di errore
        response = {
            'statusCode': 404,
            'body': json.dumps({'error': 'User not found'})
        }
    except Exception as e:
        # Gestisci altri errori
        response = {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }

    return response


"""


"""



from flask import Flask, request, jsonify
from pynamodb.models import Model
from pynamodb.attributes import UnicodeAttribute, NumberAttribute
from pynamodb.exceptions import PutError, DoesNotExist

# Definisci la classe del modello User
class User(Model):
    class Meta:
        table_name = 'Users'
    user_id = UnicodeAttribute(hash_key=True)
    name = UnicodeAttribute()
    email = UnicodeAttribute()

# Inizializza l'app Flask
app = Flask(__name__)

# Definisci l'endpoint per la creazione dell'utente
@app.route('/create-user', methods=['POST'])
def create_user():
    try:
        user_data = request.json
        user = User(
            user_id=user_data['user_id'],
            name=user_data['name'],
            email=user_data['email']
        )
        user.save()
        return jsonify({'message': 'User created successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Definisci l'endpoint per la visualizzazione dell'utente per ID
@app.route('/user/<user_id>', methods=['GET'])
def get_user_by_id(user_id):
    try:
        user = User.get(user_id)
        user_info = {
            'user_id': user.user_id,
            'name': user.name,
            'email': user.email
        }
        return jsonify(user_info), 200
    except DoesNotExist:
        return jsonify({'error': 'User not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Avvia l'app Flask
if __name__ == '__main__':
    app.run(debug=True)

"""




#definizione delle rotte API


from flask import Flask, request, jsonify
import json
from pynamodb.models import Model
from pynamodb.attributes import UnicodeAttribute
from pynamodb.exceptions import PutError, DoesNotExist

app = Flask(__name__)

# Lista di utenti (simulata)
users = []

# Route API per la creazione di un nuovo utente
@app.route('/users', methods=['POST'])
def create_user():
    user_data = request.json
    if 'user_id' in user_data and 'name' in user_data and 'email' in user_data:
        users.append(user_data)
        return jsonify({'message': 'User created successfully'}), 201
    else:
        return jsonify({'error': 'Missing required user data'}), 400

# Route API per ottenere un utente per ID
@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    for user in users:
        if user['user_id'] == user_id:
            return jsonify(user), 200
    return jsonify({'error': 'User not found'}), 404

if __name__ == '__main__':
    app.run(debug=True)
























"""

# Definizione del modello User
class User(Model):
    class Meta:
        table_name = 'NomeDellaTuaTabellaUser'
        region = 'us-east-1'

    user_id = UnicodeAttribute(hash_key=True)
    name = UnicodeAttribute()
    email = UnicodeAttribute()

# Funzione per creare un nuovo utente
def createUser(event, context):
    try:
        # Ottenere i dati dell'utente dal corpo della richiesta
        user_data = json.loads(event['body'])

        # Creare un nuovo utente utilizzando i dati ricevuti
        user = User(
            user_id=user_data['user_id'],
            name=user_data['name'],
            email=user_data['email']
        )
        user.save()

        # Costruisci la risposta
        response = {
            'statusCode': 200,
            'body': json.dumps({'message': 'User created successfully'})
        }
    except KeyError:
        # Se i dati dell'utente non sono completi, restituisci un messaggio di errore
        response = {
            'statusCode': 400,
            'body': json.dumps({'error': 'Missing required user data'})
        }
    except PutError as e:
        # Se si verifica un errore durante il salvataggio dell'utente, restituisci un messaggio di errore
        response = {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }
    except Exception as e:
        # Gestisci altri errori
        response = {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }

    return response

    """
