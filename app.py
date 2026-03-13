from flask import Flask, request, jsonify, send_file
import img2pdf
from PIL import Image
import io, base64, os
from pypdf import PdfMerger # <- Nuova importazione per unire i PDF

app = Flask(__name__)

# --- IL TUO ENDPOINT ORIGINALE PER LE IMMAGINI ---
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

# --- NUOVO ENDPOINT PER UNIRE I PDF IN BASE64 ---
@app.route('/merge', methods=['POST'])
def merge_pdfs():
    try:
        data = request.get_json()
        pdf_strings = data.get('files', [])
        
        if not pdf_strings:
            return jsonify({"error": "Nessun file ricevuto"}), 400

        merger = PdfMerger()
        
        for b64_string in pdf_strings:
            # Pulisce la stringa se n8n ha aggiunto "data:application/pdf;base64," all'inizio
            if "," in b64_string:
                b64_string = b64_string.split(",")[1]
            
            # Decodifica la stringa Base64 e la aggiunge al "frullatore" dei PDF
            pdf_bytes = base64.b64decode(b64_string)
            merger.append(io.BytesIO(pdf_bytes))
        
        # Prepara il file finale in memoria
        output = io.BytesIO()
        merger.write(output)
        merger.close()
        output.seek(0)
        
        # Restituisce il PDF direttamente come file fisico scaricabile
        return send_file(
            output, 
            mimetype='application/pdf', 
            download_name='documento_unito.pdf'
        )
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# --- ENDPOINT DI HEALTH ---
@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'ok'})

if __name__ == '__main__':
    # Railway inietta la porta dinamicamente, usiamo 8080 come fallback
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)
