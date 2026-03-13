from flask import Flask, request, send_file
import img2pdf
from PIL import Image
import io
import base64

app = Flask(__name__)

@app.route('/convert', methods=['POST'])
def convert():
    data = request.json
    images = data.get('images', [])
    
    image_bytes_list = []
    for img_b64 in images:
        img_bytes = base64.b64decode(img_b64)
        img = Image.open(io.BytesIO(img_bytes)).convert('RGB')
        buf = io.BytesIO()
        img.save(buf, format='JPEG', quality=90)
        image_bytes_list.append(buf.getvalue())
    
    pdf_bytes = img2pdf.convert(image_bytes_list)
    pdf_b64 = base64.b64encode(pdf_bytes).decode('utf-8')
    
    return {'pdf': pdf_b64, 'pages': len(image_bytes_list)}

@app.route('/health', methods=['GET'])
def health():
    return {'status': 'ok'}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
```

---

**`requirements.txt`**
```
flask
img2pdf
Pillow
gunicorn
