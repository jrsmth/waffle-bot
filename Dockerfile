FROM python:3.11-slim
WORKDIR /code
COPY src/requirements.txt /code
RUN pip3 install -r requirements.txt --no-cache-dir
COPY . /code
ENV PYTHONUNBUFFERED=0
ENV FLASK_ENV=prod
EXPOSE 8080
ENTRYPOINT ["gunicorn", "-b", "0.0.0.0:3000", "-k", "gevent", "-w", "1", "--chdir", "src", "app:app"]
