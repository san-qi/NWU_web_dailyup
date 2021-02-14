FROM python:3.6-slim

WORKDIR /usr/src/app

COPY . .
RUN pip install --no-cache-dir -r requirements.txt

CMD ["gunicorn", "-w", "2", "-b", ":5000", "app:app"]
