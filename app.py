import base64
import io
from flask import Flask, request, send_file
from PyPDF2 import PdfMerger

app = Flask(__name__)

@app.route('/merge', methods=['POST'])
def merge_pdfs():
    # Riceve un JSON con una lista di stringhe base64
    data = request.get_json()
    pdf_strings = data.get('files', [])
    
    merger = PdfMerger()
    
    for b64_string in pdf_strings:
        # Decodifica la stringa e la trasforma in un file "virtuale"
        pdf_bytes = base64.b64decode(b64_string)
        merger.append(io.BytesIO(pdf_bytes))
    
    output = io.BytesIO()
    merger.write(output)
    output.seek(0)
    
    return send_file(output, mimetype='application/pdf')

if __name__ == '__main__':
    # Configurazione specifica per Railway sulla porta 8080
    app.run(host='0.0.0.0', port=8080)
