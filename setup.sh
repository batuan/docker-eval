docker-compose up --build -d
echo "Sleep 5 seconds to wait for all tests to finish"
sleep 5
docker-compose logs --no-color >& logs_docker_compose.txt

echo "remove all docker container"
docker-compose down