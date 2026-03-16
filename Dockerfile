FROM nikolaik/python-nodejs:python3.11-nodejs20

RUN pip install flask img2pdf Pillow gunicorn pypdf

WORKDIR /app
COPY app.py .

CMD ["sh", "-c", "gunicorn --bind 0.0.0.0:${PORT:-8080} --timeout 300 --workers 2 app:app"]
