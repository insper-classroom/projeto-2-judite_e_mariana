from servidor import *
from unittest.mock import patch

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
