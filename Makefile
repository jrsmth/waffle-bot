make install:
	pip3 install -r src/app/requirements.txt

make start:
	docker-compose up -d --build

make redis:
	docker run --name waffle-redis -p 6379:6379 -d redis

make stop:
	docker-compose down

make test:
	python3 -m pytest src
