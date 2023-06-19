# Docker Report
## 1. Python test
There are 3 test: 

 1. Test authentification with API: `/permissions` and the params are: `username, password` which have reponse status `200` or `403`
```python
users_pass = [('alice', 'wonderland', 200), ('bob', 'builder', 200), ('clementine', 'mandarine', 403)]
    
for  username, password, expected_code  in  users_pass:
    r = requests.get(
        url='http://{address}:{port}/permissions'.format(address=api_address, port=api_port),
                params= {'username': username,
                        'password': password})

status_code = r.status_code
if  status_code == expected_code:
    test_status = 'SUCCESS'

else:
    test_status = 'FAILURE'
```
 2. Test authorization with API `v1/sentiment` or `v2/sentiment` and the params are: `username, password, sentence (test)` and the reponse code is 200 or 403

```python
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
```
 3. Test content with API `v1/sentiment` or `v2/sentiment` and the params are: `username, passsword, sentence (one positive, one negative)` this API return a `score`, which `score>0.5` mean this sentence is positive, and `score <=0.5` mean negative

```python
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
```

The api_address is `localhost`

## 2. Docker compose
1. Create a Dockerfile to build 3 container for testing. In this Exam, I used `network_mode: host` to make all containers run on `localhost`. This is not **best practices** but I think I is okey for a homework.

```bash
FROM  datascientest/fastapi:1.0.0
RUN  mkdir  -p  /script
WORKDIR  /script
```
I use the workdir is `/script` where I can put all python code and sync the `log.txt` file

2. Docker-compose
In the docker compose has 4 containers: `fastapi`, `test_authentification`, `test_author`,  `test_content`. The 3 test containers is build from `Dockerfile` 

```yml
version: "3.9"
services:
  fast_api:
    image: datascientest/fastapi:1.0.0
    network_mode: "host"
    
  test_authentication:
    build: ./
    container_name: test_authentication
    network_mode: "host"
    command: bash -c "sleep 1 && pwd && ls && python3 test_authentication.py"
    depends_on:
      - fast_api
    volumes:
      - ./python_script:/script
    environment:
      - LOG=1
    ...
```
## 3. Result
In total there are 11 tests

```
TEST Time: 2023-05-17 12:06:41.749417
============================
    Content test
============================
request done at "/v2/sentiment"
| username="alice"
| password="wonderland"
| sentence="life is beautiful"
expected sentence positive
actual restult = positive
==>  SUCCESS

TEST Time: 2023-05-17 12:06:41.752933
============================
    Content test
============================
request done at "/v2/sentiment"
| username="alice"
| password="wonderland"
| sentence="that sucks"
expected sentence negative
actual restult = negative
==>  SUCCESS
```
The detail result can be found at `python_script/log.txt`

## 4. How to run
`./setup.sh`

```bash
docker-compose up --build -d
echo "Sleep 5 seconds to wait for all tests to finish"
sleep 5
docker-compose logs --no-color >& logs_docker_compose.txt

echo "remove all docker container"
docker-compose down
```