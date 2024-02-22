import json
from pynamodb.models import Model
from pynamodb.attributes import UnicodeAttribute,NumberAttribute
from pynamodb.exceptions import PutError, DoesNotExist



class User(Model):
    class Meta:
        table_name = 'Users'
        region = 'us-east-1'

    user_id = NumberAttribute(hash_key=True)
    name = UnicodeAttribute()
    email = UnicodeAttribute()

class Counter(Model):
    class Meta:
        table_name = 'Users'
        region = 'us-east-1'

    counter_id = UnicodeAttribute(hash_key=True)
    current_id = NumberAttribute(default=0)

# Inizializzazione del contatore degli ID degli utenti
def initialize_counter():
    try:
        counter = Counter.get('user_counter')
    except Counter.DoesNotExist:
        counter = Counter(
            counter_id='user_counter',
            current_id=0
        )
        counter.save()

# Funzione per creare un nuovo utente
def create_user(event, context):
    try:
        # Inizializza il contatore se non esiste già
        initialize_counter()

        # Ottieni il valore corrente del contatore degli ID dalla tabella DynamoDB
        counter = Counter.get('user_counter')
        current_id = counter.current_id

        # Incrementa il contatore
        counter.current_id += 1
        counter.save()

        # Utilizza il valore corrente del contatore come ID per il nuovo utente
        user_id = str(current_id)

        # Ottenere i dati dell'utente dalla richiesta
        user_data = json.loads(event['body'])

        # Verifica che la richiesta contenga almeno un nome e un'email
        if 'name' not in user_data or 'email' not in user_data:
            return {
                'statusCode': 400,
                'body': json.dumps({'error': 'Name and email are required'})
            }

        # Creare un nuovo utente nella tabella DynamoDB utilizzando PynamoDB
        user = User(
            user_id=user_id,
            name=user_data['name'],
            email=user_data['email']
        )
        user.save()

        return {
            'statusCode': 200,
            'body': json.dumps({'message': 'User created successfully', 'user_id': user_id})
        }

    except PutError as e:  # Gestisci specificamente l'errore di inserimento
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }


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