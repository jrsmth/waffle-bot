FROM python:3.11-slim
WORKDIR /code
COPY src/requirements.txt /code
RUN pip3 install -r requirements.txt --no-cache-dir
COPY . /code
ENV PYTHONUNBUFFERED=0
ENV FLASK_ENV=local
ENV BOT_TOKEN=thisisatoken
ENV VERIFICATION_TOKEN=thisisatoken
ENV SLACK_SIGNING_SECRET=thisisatoken
ENV REDIS_TOKEN=thisisatoken
ENV REDIS_URL="redis://@redis:6379/0"
EXPOSE 8080 3000
ENTRYPOINT ["gunicorn", "-b", "0.0.0.0:3000", "-k", "gevent", "-w", "1", "--chdir", "src", "app:app"]
