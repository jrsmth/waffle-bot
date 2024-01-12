env = "dev"
# local : make sure local redis is running
# dev   : ensure IP is whitelisted on render redis
# prod
make start:
	export FLASK_ENV=$(env) && gunicorn -b 0.0.0.0:3000 -k gevent -w 1 --chdir src app:app

make install:
	pip3 install -r ./src/requirements.txt
