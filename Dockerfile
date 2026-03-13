FROM nikolaik/python-nodejs:python3.11-nodejs20

RUN pip install flask img2pdf Pillow gunicorn

WORKDIR /app
COPY app.py .

EXPOSE $PORT

CMD ["sh", "-c", "gunicorn --bind 0.0.0.0:$PORT app:app"]
