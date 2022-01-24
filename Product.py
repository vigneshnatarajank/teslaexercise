import json
from datetime import datetime
from io import BytesIO
import pandas as pd
from flask import Flask, jsonify, request, send_file
import requests

# creating a Flask app
app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    if (request.method == 'GET'):
        data = "hello world"
        return jsonify({'data': data})


@app.route('/get_product_info/<product_id>', methods=['GET'])
def get_product_id(product_id):
    if product_id.isdigit():
        result = requests.get('https://reqres.in/api/products/' + str(product_id))
        if result.ok:
            result = json.loads(result.text)
            if int(product_id) >= 5:
                result['data']['EVALUATION'] = 'TESTING'
            return result
        elif result.status_code == 404:
            return jsonify({'ID': product_id, 'note': 'No data available'})
    else:
        return jsonify({'Error Code': 405, 'Error Message': 'Invalid Parameter'}), 405


@app.route('/get_download_product/<product_id>', methods=['GET'])
def get_download_product(product_id):
    if product_id.isdigit():
        result = requests.get('https://reqres.in/api/products/' + str(product_id))
        if result.ok:
            result = json.loads(result.text)['data']
            result['download_time'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            df = pd.DataFrame([result])
            output = BytesIO()
            writer = pd.ExcelWriter(output, engine='xlsxwriter')

            df.to_excel(writer, startrow=0, merge_cells=False, sheet_name="Sheet_1", index=False)
            workbook = writer.book
            worksheet = writer.sheets["Sheet_1"]
            format = workbook.add_format()
            format.set_bg_color('#eeeeee')
            worksheet.set_column(0,9,28)

            writer.close()

            output.seek(0)
            return send_file(output, attachment_filename="Product_Download_" + str(product_id) + ".xlsx", as_attachment=True)
        elif result.status_code == 404:
            return jsonify({'ID': product_id, 'note': 'No data available'})
    else:
        return jsonify({'Error Code': 405, 'Error Message': 'Invalid Parameter'}), 405

# driver function
if __name__ == '__main__':
    app.run(debug=True)