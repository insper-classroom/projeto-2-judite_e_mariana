from servidor import *
from unittest.mock import patch, MagicMock
import pytest
import json
import requests

@pytest.fixture
# Cria um cliente de teste para a API
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


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


def test_get_imovel_por_id_existente(client):
    # Teste retorna 200 com os atributos do imóvel

    with patch('servidor.connect_db') as mock_connect_db:

        # Mock para a conexão e o cursor
        mock_conn = MagicMock()
        mock_cursor = MagicMock()

        # Mock para retornar o cursor quando chamarmos conn.cursor()
        mock_connect_db.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor

        # Simula o banco retornando o primeiro imóvel
        mock_cursor.fetchone.return_value = DICIONARIO_IMOVEIS[0]

        # Faz a requisição para a API
        response = client.get("/imoveis/1")

    # Verifica a resposta
    assert response.status_code == 200
    assert response.get_json() == DICIONARIO_IMOVEIS[0]