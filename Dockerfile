FROM python:3.11.4

WORKDIR /csv-aggregator

COPY . .

RUN pip install --no-cahce-dir -r requirements.txt

EXPOSE 5000

CMD ["python", "./app.py"]