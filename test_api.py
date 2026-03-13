from servidor import *
from unittest.mock import patch
import pytest
import json
import requests

DICIONARIO_IMOVEIS = [
        {
            'id': int(1),
            'logradouro': 'Nicole Common',
            'tipo_logradouro': 'Travessa',
            'bairro': 'Lake Danielle',
            'cidade': 'Judymouth',
            'cep': '85184',
            'tipo': 'casa em condominio',
            'valor': float(488424),
            'data_aquisicao': '2017-07-29',
        },
        {
            'id': int(2),
            'logradouro': 'Price Prairie',
            'tipo_logradouro': 'Travessa',
            'bairro': 'Colonton',
            'cidade': 'North Garyville',
            'cep': '93354',
            'tipo': 'casa em condominio',
            'valor': float(260070),
            'data_aquisicao': '2021-11-30',  
        }
]


#testar função que lista todos os imoveis e seus atributos
def test_listar_imoveis():
    with patch('servidor.listar_imoveis', DICIONARIO_IMOVEIS):
        response = client.get('/imoveis')
        response_json = response.get_json()
        assert response.status_code == 200
        for k in response_json.keys():
            assert response_json[k] == DICIONARIO_IMOVEIS[0][k]