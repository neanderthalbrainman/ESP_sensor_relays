cd ~/dockers/mysql
docker compose up -d


echo "To login to mysql:"
echo "docker exec -it mysql-test1 mysql -u user -p"

cd ~/Documents/RF24/pyRF24
source venv/bin/activate
python3 ~/Documents/NRF_py/ingest_relays.py
