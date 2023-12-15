
from datetime import datetime, timedelta
from flask import request

import dateutil.relativedelta
 
def data_inicio_e_fim(rota):
    formato_data_input = "%d/%m/%Y"
    data_fim_padrao = datetime.now()

    if rota == "dc":
        data_inicio_padrao = data_fim_padrao.replace(day=1)
    elif rota == "sac":
        data_inicio_padrao = data_fim_padrao - timedelta(days=15)
    else:
        data_inicio_padrao = data_fim_padrao - dateutil.relativedelta.relativedelta(months=2)

    data_inicio_str = request.args.get('data_inicio', default=data_inicio_padrao.strftime(formato_data_input), type=str)
    data_fim_str = request.args.get('data_fim', default=data_fim_padrao.strftime(formato_data_input), type=str)

    # Função para validar a data
    def validar_data(data_str, nome_data):
        try:
            datetime.strptime(data_str, formato_data_input)
        except ValueError:
            raise ValueError(f"Formato de data inválido para {nome_data} ('{data_str}'). O formato esperado é DD/MM/AAAA.")

    validar_data(data_inicio_str, "data_inicio")
    validar_data(data_fim_str, "data_fim")

    # Datas estão no formato correto, prosseguir
    data_inicio = datetime.strptime(data_inicio_str, formato_data_input)
    data_fim = datetime.strptime(data_fim_str, formato_data_input)

    return data_inicio.strftime(formato_data_input), data_fim.strftime(formato_data_input)


       