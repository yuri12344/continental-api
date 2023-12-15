# -*- encoding: utf-8 -*-

from utils.corpem_data_getter import CorpemDataService
from utils import data_inicio_e_fim
from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/dc/')
def get_dc():
    try:
        data_inicio, data_fim = data_inicio_e_fim("dc")
    except ValueError as e:
        return str(e)
    
    corpem_data_getter = CorpemDataService()
    data = corpem_data_getter.get_data(data_inicio, data_fim)
    return jsonify(data), 200, {'Content-Type': 'application/json; charset=utf-8'}
    
@app.route('/dc/')
def get_sac():
    try:
        data_inicio, data_fim = data_inicio_e_fim("sac")
    except ValueError as e:
        return str(e)
    
    corpem_data_getter = CorpemDataService()
    data = corpem_data_getter.get_data(data_inicio, data_fim)
    return jsonify(data), 200, {'Content-Type': 'application/json; charset=utf-8'}
    
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)