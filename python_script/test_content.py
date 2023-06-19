import os
import requests

# définition de l'adresse de l'API
api_address = 'localhost'
# port de l'API
api_port = 8000

# requête

url='http://{api_address}:{api_port}/{version}/sentiment'

# r = requests.get(
#     url=url.format(version=),
#     params= {
#         'username': 'alice',
#         'password': 'wonderland'
#     }
# )

output = '''
============================
    Content test
============================

request done at "/{version}/sentiment"
| username="alice"
| password="wonderland"
| sentence="{sentence}"

expected sentence {expected}
actual restult = {result}

==>  {test_status}

'''

versions=['v1', 'v2']
sentences_ex=[('life is beautiful', 'positive'), ('that sucks', 'negative')]

for version in versions:
    # test1
    for sentence, expected in sentences_ex:
        r = requests.get(
            url=url.format(api_address=api_address, api_port=api_port, version=version), 
            params={
                'username': 'alice',
                'password': 'wonderland',
                'sentence': sentence
        })

        # print(r.text)

        if r.json()['score'] > 0.5:
            result='positive'
        else:
            result='negative'
        
        if result==expected:
            test_status = 'SUCCESS'
        else:
            test_status = 'FAILURE'
        
        output_print = output.format(version=version, sentence=sentence, 
                            expected=expected, result=result, test_status=test_status)
        print(output_print)

        # impression dans un fichier
        if os.environ.get('LOG') == '1':
            print('write to file')
            with open('log.txt', 'a') as file:
                import datetime
                file.write('TEST Time: {}'.format(datetime.datetime.now()))
                file.write(output_print)
                print("=================================================")



