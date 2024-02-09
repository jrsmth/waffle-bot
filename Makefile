make install:
	pip3 install -r requirements.txt

make start:
	docker-compose up -d --build

make stop:
	docker-compose down

make test:
	python3 -m pytest -s -v
