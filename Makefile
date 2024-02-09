make install:
	pip3 install -r requirements.txt

make start:
	docker-compose up -d --build

make stop:
	docker-compose down

make test:
	python -m pytest -s -v
