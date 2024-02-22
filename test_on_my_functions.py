import json
import pytest
from unittest.mock import patch
from user_functions import create_user, getUserById
from unittest.mock import MagicMock

@patch('user_functions.User')
@patch('user_functions.Counter')
def test_create_user(mock_Counter, mock_User):
    # Definire l'input event per la funzione Lambda
    event = {
        'body': '{"name": "John Doe", "email": "john.doe@example.com"}'
    }

    # Mockare il comportamento del Counter.get() per simulare l'inizializzazione del contatore
    mock_Counter.get.return_value = mock_Counter
    mock_Counter.current_id = 1

    # Mockare il salvataggio dell'utente
    mock_User.save.return_value = None

    # Chiamare la funzione Lambda e ottenere il risultato
    result = create_user(event, None)

    # Verificare che lo status code sia 200 e che il messaggio di successo sia presente nel body
    assert result['statusCode'] == 200
    assert json.loads(result['body']) == {'message': 'User created successfully', 'user_id': '1'}

    
@patch('user_functions.User')
def test_getUserById(mock_User):
    # Simulate user data
    mock_user_instance = mock_User.return_value
    mock_user_instance.user_id = '1'
    mock_user_instance.name = 'joele'
    mock_user_instance.email = 'joele@example.com'
    
    # Simulate event data
    event = {
        'pathParameters': {
            'user_id': '1'
        }
    }

    # Call your function with simulated event and None for context
    result = getUserById(event, None)

    # Define the expected body based on the mock user data
    expected_body = {
        'user_id': mock_user_instance.user_id ,
        'name':  mock_user_instance.name ,
        'email': mock_user_instance.email
    }

    # Assert that the result matches the expected body
    assert result['statusCode'] == 200
    assert json.loads(result['body']) == expected_body