import os
import requests

# définition de l'adresse de l'API
api_address = 'localhost'
# port de l'API
api_port = 8000

# requête

output = '''
============================
    Authorization test
============================

request done at "/{version}/sentiment"
| username="{username}"
| password="{password}"

expected authorization result = {experted_code}
actual restult = {status_code}

==>  {test_status}

'''

user_pass_expect=[('alice', 'wonderland', 'v1', 200),('alice', 'wonderland', 'v2', 200),
                  ('bob', 'builder', 'v1', 200), ('bob', 'builder', 'v2', 403) ]

for username, password, version, experted_code in user_pass_expect:

    r = requests.get(
        url='http://{address}:{port}/{version}/sentiment'.format(address=api_address, 
                                                                 port=api_port, version=version),
        params= {
            'username': username,
            'password': password,
            'sentence': 'test'
        }
    )

    # statut de la requête
    status_code = r.status_code

    # affichage des résultats
    if status_code==experted_code:
        test_status = 'SUCCESS'
    else:
        test_status = 'FAILURE'

    output_print = output.format(version=version, username=username, password=password,
                                 experted_code=experted_code, status_code=status_code, test_status=test_status)
    print(output_print)

    # impression dans un fichier
    if os.environ.get('LOG') == '1':
        print('write to file')
        with open('log.txt', 'a') as file:
            import datetime
            file.write('TEST Time: {}'.format(datetime.datetime.now()))
            file.write(output_print)
            print("=================================================")