# -*- encoding: utf-8 -*-
import ftfy

from decouple import config

import requests
import re
import json
import ujson


CORPEM_API_URL_PROD = config('CORPEM_API_URL')

class CorpemDataService:
    def write_to_a_file(self, text, filename='data.json'):
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(text)
            
    def treat_response_corpem(self, text):
        texto_corrigido = ftfy.fix_text(text)

        # Remove ou substitui caracteres de controle, exceto quebras de linha e tabulações
        texto_corrigido = re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f\x7f-\x9f]', '', text)

        # Corrige vírgulas extras antes de fechamentos de chaves em JSON.
        texto_corrigido = re.sub(r',\s*}', '}', texto_corrigido)

        # Remove sequências de escape incorretos, exceto as comuns como \n, \t, etc.
        texto_corrigido = re.sub(r'\\(?!["\\/bfnrtu])', '', texto_corrigido)

        # Substitui quebras de linha (\n) e tabulações (\t) por espaços
        texto_corrigido = re.sub(r'[\n\t]+', ' ', texto_corrigido)

        # Substitui espaços não padrão (como espaço não quebrável) por espaços comuns
        texto_corrigido = re.sub(r'\u00A0+', ' ', texto_corrigido)


        return texto_corrigido

    def get_data(self, data_inicio, data_fim):
        body = {
            "CORPEM_TMS_NR": {
                "DT_EMI_INI": data_inicio,
                "DT_EMI_FIM": data_fim
            }
        }
        headers = {"Content-Type": "application/json; charset=utf-8"}
        response = requests.post(CORPEM_API_URL_PROD, json=body, headers=headers)

        # Decodificar a resposta
        resposta_corpem = response.content.decode('latin1')

        # Tratar o texto
        texto_tratado = self.treat_response_corpem(resposta_corpem)
        
        # Carregar o JSON
        try:
            data = ujson.loads(texto_tratado)
        except json.JSONDecodeError as e:
            print(f"Erro ao decodificar JSON: {e}")
            return None

        return data

