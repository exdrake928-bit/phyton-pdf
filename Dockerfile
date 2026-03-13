FROM nikolaik/python-nodejs:python3.11-nodejs20

RUN pip install flask img2pdf Pillow gunicorn

WORKDIR /app
COPY app.py .

EXPOSE 5000

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]
