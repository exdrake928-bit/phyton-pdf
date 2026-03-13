from flask import Flask, request, jsonify
import img2pdf
from PIL import Image
import io, base64, os
from pypdf import PdfWriter

app = Flask(__name__)

@app.route('/convert', methods=['POST'])
def convert():
    files = request.files.getlist('images')
    image_bytes_list = []
    for file in files:
        img = Image.open(file.stream).convert('RGB')
        buf = io.BytesIO()
        img.save(buf, format='JPEG', quality=90)
        image_bytes_list.append(buf.getvalue())
    pdf_bytes = img2pdf.convert(image_bytes_list)
    pdf_b64 = base64.b64encode(pdf_bytes).decode('utf-8')
    return jsonify({'pdf': pdf_b64, 'pages': len(image_bytes_list)})

@app.route('/merge', methods=['POST'])
def merge():
    data = request.json
    pdfs = data.get('pdfs', [])
    writer = PdfWriter()
    for pdf_b64 in pdfs:
        pdf_bytes = base64.b64decode(pdf_b64)
        writer.append(io.BytesIO(pdf_bytes))
    output = io.BytesIO()
    writer.write(output)
    pdf_b64 = base64.b64encode(output.getvalue()).decode('utf-8')
    return jsonify({'pdf': pdf_b64, 'pages': writer.get_num_pages()})

@app.route('/health', methods=['GET'])
de
