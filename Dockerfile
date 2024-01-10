FROM python:3.11-slim
WORKDIR ./src
RUN pip3 install -r requirements.txt --no-cache-dir
ENV PYTHONUNBUFFERED=0
EXPOSE 3000
ENTRYPOINT ["python3", "app.py"]
