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

# variavel global para simular o banco de dados
DICIONARIO_IMOVEIS = { 'imoveis': [
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
] }

@patch("servidor.connect_db")
def test_get_imoveis(mock_connect_db, client):
    # Criandos um Mock para a conexão e o cursor
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    
    # Configurandos o Mock para retornar o cursor quando chamarmos conn.cursor()
    mock_conn.cursor.return_value = mock_cursor
    
    # Simulando o retorno do banco de dados
    mock_cursor.fetchall.return_value = [ (1, 'Nicole Common', 'Travessa', 'Lake Danielle', 'Judymouth', '85184', 'casa em condominio', 488424, '2017-07-29'),
                                        (2, 'Price Prairie', 'Travessa', 'Colonton', 'North Garyville', '93354', 'casa em condominio', 260070, '2021-11-30') 
                                        ]
    
    # Substituíndo a função `connect_db` para retornar nosso Mock em vez de uma conexão real
    mock_connect_db.return_value = mock_conn
    
    # Fazendo requisição para a api
    response = client.get('/imoveis')
    
    #verificando se o código de status retornou 200
    assert response.status_code == 200
    
    # Verificando se os dados retornados estão corretos
    expected_response = DICIONARIO_IMOVEIS
    assert response.get_json() == expected_response

    # Verificando se a consulta SQL foi executada corretamente
    mock_cursor.execute.assert_called_once_with("SELECT * FROM imoveis")

@patch("servidor.connect_db")
def test_get_imoveis_vazio(mock_connect_db, client):
    # Criandos um Mock para a conexão e o cursor
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_conn.cursor.return_value = mock_cursor

    # Simulando que o banco de dados não retorna nenhum imovel
    mock_cursor.fetchall.return_value = []

    mock_connect_db.return_value = mock_conn

    # Fazendo a requisição para a API
    response = client.get("/imoveis")

    # Verificando se o código de status da resposta é 404 e se a mensagem de erro está correta
    assert response.status_code == 404
    assert response.get_json() == {"erro": "Nenhum imovel encontrado"}
    

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
   
@patch("servidor.connect_db") 
def test_new_imovel(mock_connect_db, client):
    # Criandos um Mock para a conexão e o cursor
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    
    # Configurandos o Mock para retornar o cursor quando chamarmos conn.cursor()
    mock_conn.cursor.return_value = mock_cursor
    
    # Substituíndo a função `connect_db` para retornar nosso Mock em vez de uma conexão real
    mock_connect_db.return_value = mock_conn
    
    # Dados que serão enviados para a API
    new_imovel = {
        'logradouro': 'Taylor Ranch',
        'tipo_logradouro': 'Avenida',
        'bairro': 'West Jennashire',
        'cidade': 'Katherinefurt',
        'cep': '51116',
        'tipo': 'apartamento',
        'valor': 815970,
        'data_aquisicao': '2020-04-24'
    }
    
    # Fazendo requisição para a api
    response = client.post('/submit', json=new_imovel)
    
    # verificando se o código de status retornou 200
    assert response.status_code == 200
    
    # Verificando se os dados retornados estão corretos
    expected_response = {
        'id': int(3),
        'logradouro': 'Taylor Ranch',
        'tipo_logradouro': 'Avenida',
        'bairro': 'West Jennashire',
        'cidade': 'Katherinefurt',
        'cep': '51116',
        'tipo': 'apartamento',
        'valor': float(815970),
        'data_aquisicao': '2020-04-24'
    }

    assert response.get_json() == expected_response

    # Verificandos se a consulta SQL foi executada corretamente
    mock_cursor.execute.assert_called_once_with(
        "INSERT INTO imoveis (logradouro, tipo_logradouro, bairro, cidade, cep, tipo, valor, data_aquisicao) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
        (
            'Taylor Ranch',
            'Avenida',
            'West Jennashire',
            'Katherinefurt',
            '51116',
            'apartamento',
            815970,
            '2020-04-24'
        )
    )
    
    # Verificando se a transação foi confirmada
    mock_conn.commit.assert_called_once()
    
@patch("servidor.connect_db")
def test_new_imovel_vazio(mock_connect_db, client):
    # Criandos um Mock para a conexão e o cursor
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    
    # Configurandos o Mock para retornar o cursor quando chamarmos conn.cursor()
    mock_conn.cursor.return_value = mock_cursor
    
    # Substituíndo a função `connect_db` para retornar nosso Mock em vez de uma conexão real
    mock_connect_db.return_value = mock_conn
    
    # Dados vazios que serão enviados para a API
    new_imovel_vazio = {}
    
    # Fazendo requisição para a api
    response = client.post('/submit', json=new_imovel_vazio)
    
    # verificando se o código de status retornou 400
    assert response.status_code == 400
    
    # Verificando se os dados retornados estão corretos
    expected_response = {"erro": "Dados incompletos"}
    assert response.get_json() == expected_response
    
    # Verificando se nenhuma consulta SQL foi executada
    mock_cursor.execute.assert_not_called()