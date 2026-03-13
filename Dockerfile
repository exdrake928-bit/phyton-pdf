FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY app.py .

EXPOSE 5000

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]
```

---

## Deploy su Railway

1. Crea una **nuova cartella** nel repo GitHub chiamata `pdf-converter`
2. Aggiungi i 3 file sopra
3. Su Railway → **New Service** → **GitHub Repo** → seleziona la cartella `pdf-converter`
4. Railway assegnerà un URL tipo `pdf-converter.up.railway.app`

---

## Nodo n8n

Poi in n8n sostituisci iLovePDF con un **HTTP Request** verso:
```
POST https://pdf-converter.up.railway.app/convert
