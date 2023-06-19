import os
import requests

# définition de l'adresse de l'API
api_address = 'localhost'
# port de l'API
api_port = 8000

output = '''
============================
    Authentication test
============================

request done at "/permissions"
| username={username}
| password={password}

expected result = {expected_code}
actual restult = {status_code}

==>  {test_status}

'''

users_pass = [('alice', 'wonderland', 200), ('bob', 'builder', 200), ('clementine', 'mandarine', 403)]

for username, password, expected_code in users_pass:
    r = requests.get(
        url='http://{address}:{port}/permissions'.format(address=api_address, port=api_port),
        params= {
            'username': username,
            'password': password
        }
    )

    # statut de la requête
    status_code = r.status_code

    # affichage des résultats
    if status_code == expected_code:
        test_status = 'SUCCESS'
    else:
        test_status = 'FAILURE'
    
    output_print = output.format(status_code=status_code, test_status=test_status,
                    expected_code=expected_code, username=username, password=password)
    print(output_print)

    # impression dans un fichier
    print(os.environ.get('LOG'))
    
    if os.environ.get('LOG') == '1':
        print('write to file')
        with open('log.txt', 'a') as file:
            import datetime
            file.write('TEST Time: {}'.format(datetime.datetime.now()))
            file.write(output_print)
            print("=================================================")