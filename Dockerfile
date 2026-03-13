FROM nikolaik/python-nodejs:python3.11-nodejs20

RUN pip install img2pdf Pillow

RUN npm install -g n8n

EXPOSE 5678

CMD ["n8n", "start"]
