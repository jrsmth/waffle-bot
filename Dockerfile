FROM python:3.11-slim
WORKDIR /code
COPY src/requirements.txt /code
RUN pip3 install -r requirements.txt --no-cache-dir
COPY . /code
ENV PYTHONUNBUFFERED=0
ENV ENV=prod
EXPOSE 8080
ENTRYPOINT ["python3", "src/app.py"]
