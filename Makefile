# Check if OS is Windows
ifeq ($(OS),Windows_NT)
	PYTHON := python
	PIP := pip
else
	PYTHON := python3
	PIP := pip3
endif

make install:
	$(PIP) install -r src/app/requirements.txt

make start:
	docker-compose up -d --build

make redis:
	docker run --name waffle-redis -p 6379:6379 -d redis

make stop:
	docker-compose down

make test:
	$(PYTHON) -m pytest src
