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
    
    
@patch("servidor.connect_db")
def test_get_imoveis_erro_conexao(mock_connect_db, client):
    # Simula erro de conexão
    mock_connect_db.return_value = None

    # Fazendo requisição para a api
    response = client.get("/imoveis")

    # verificando se o código de status retornou 500
    assert response.status_code == 500
    assert response.get_json() == {"erro": "Erro ao conectar ao banco de dados"}
    

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
        mock_cursor.fetchone.return_value = (1, 'Nicole Common', 'Travessa', 'Lake Danielle', 'Judymouth', '85184', 'casa em condominio', 488424, '2017-07-29')

        # Faz a requisição para a API
        response = client.get("/imoveis/1")

    # Verifica a resposta
    assert response.status_code == 200
    assert response.get_json() == DICIONARIO_IMOVEIS['imoveis'][0]

def test_get_imovel_por_id_inexistente(client):
    # Retorna 404 quando o imóvel não existe
    with patch('servidor.connect_db') as mock_connect_db:

        # Mock para a conexão e o cursor
        mock_conn = MagicMock()
        mock_cursor = MagicMock()

        # Mock para retornar o cursor quando chamarmos conn.cursor()
        mock_connect_db.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor

        # Simula o banco retornando nenhum valor
        mock_cursor.fetchone.return_value = None

        # Faz a requisição para a API
        response = client.get("/imoveis/999")

    # Verifica a resposta
    assert response.status_code == 404
    assert response.get_json() == {"erro": "Imóvel não encontrado"}


def test_get_imovel_id_erro_db(client):
    # Retorna 500 quando o banco de dados falha
    with patch('servidor.connect_db') as mock_connect_db:

        # Simula falha na conexão
        mock_connect_db.return_value = None

        # Faz a requisição para a API
        response = client.get("/imoveis/999")

    # Verifica a resposta
    assert response.status_code == 500
    assert response.get_json() == {"erro": "Erro ao conectar ao banco de dados"}

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
    expected_response = {"mensagem": "Imóvel cadastrado com sucesso"}

    assert response.get_json() == expected_response

    # Verificandos se a consulta SQL foi executada corretamente
    mock_cursor.execute.assert_called_once_with(
    "INSERT INTO imoveis (logradouro, tipo_logradouro, bairro, cidade, cep, tipo, valor, data_aquisicao) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
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
    
    
@patch("servidor.connect_db")
def test_new_imovel_erro_conexao(mock_connect_db, client):
    # Simula erro de conexão
    mock_connect_db.return_value = None

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
    response = client.post("/submit", json=new_imovel)

    # verificando se o código de status retornou 500
    assert response.status_code == 500
    assert response.get_json() == {"erro": "Erro ao conectar ao banco de dados"}
    

@patch("servidor.connect_db")
def test_imovel_atualizar_com_sucesso(mock_connect_db,client):
    # Define os dados que serão enviados na requisição
    imovel_atualizado = {
        'id': int(1),
        'logradouro': 'Nicole Common',
        'tipo_logradouro': 'Travessa',
        'bairro': 'Lake Danielle',
        'cidade': 'Judymouth',
        'cep': '85184',
        'tipo': 'casa em condominio',
        'valor': float(488424),
        'data_aquisicao': '2018-07-29', 
    }

    # Configura mocks
    mock_conn = MagicMock()
    mock_cursor = MagicMock()

    mock_connect_db.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor

    # Simula o banco retornando o primeiro imóvel
    mock_cursor.fetchone.return_value = (1, 'Nicole Common', 'Travessa', 'Lake Danielle', 'Judymouth', '85184', 'casa em condominio', 488424, '2018-07-29')

    # Faz a requisição PUT
    response = client.put('/imoveis/1', json=imovel_atualizado)

    # Verifica se a resposta está certa
    assert response.status_code == 200
    assert response.get_json() == imovel_atualizado

    # Verifica se o SELECT foi executado
    mock_cursor.execute.assert_any_call("SELECT * FROM imoveis WHERE id = %s", (1,))

    # Verifica se o UPDATE foi executado com os valores certos
    mock_cursor.execute.assert_any_call("UPDATE imoveis SET logradouro = %s, tipo_logradouro = %s, bairro = %s, cidade= %s, cep = %s, tipo = %s, valor = %s, data_aquisicao = %s WHERE id = %s", 
    (
        imovel_atualizado['logradouro'],
        imovel_atualizado['tipo_logradouro'],
        imovel_atualizado['bairro'],
        imovel_atualizado['cidade'],
        imovel_atualizado['cep'],
        imovel_atualizado['tipo'],
        imovel_atualizado['valor'],
        imovel_atualizado['data_aquisicao'],
        1
    ))

    mock_conn.commit.assert_called_once()

@patch("servidor.connect_db")
def test_imovel_atualizar_nao_encontrado(mock_connect_db, client):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()

    mock_connect_db.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor

    mock_cursor.fetchone.return_value = None

    response = client.put("/imoveis/999")

    assert response.status_code == 404
    assert response.get_json() == {"erro": "Imóvel não encontrado"}

@patch("servidor.connect_db")
def test_imovel_atualizar_erro_db(mock_connect_db, client):
    mock_connect_db.return_value = None

    response = client.put("/imoveis/999")

    assert response.status_code == 500
    assert response.get_json() == {"erro": "Erro ao conectar ao banco de dados"}
    
@patch("servidor.connect_db")
def test_del_imovel(mock_connect_db, client):
    # Criandos um Mock para a conexão e o cursor
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    
    # Configurandos o Mock para retornar o cursor quando chamarmos conn.cursor()
    mock_conn.cursor.return_value = mock_cursor

    # Substituíndo a função `connect_db` para retornar nosso Mock em vez de uma conexão real
    mock_connect_db.return_value = mock_conn

    # Simula o banco retornando o primeiro imóvel
    mock_cursor.fetchone.return_value = (1, 'Nicole Common', 'Travessa', 'Lake Danielle', 'Judymouth', '85184', 'casa em condominio', 488424, '2017-07-29')

    # Fazendo requisição para a api
    response = client.delete("/imoveis/1")

    # verificando se o código de status retornou 200
    assert response.status_code == 200
    assert response.get_json() == {"mensagem": "Imóvel deletado com sucesso"}

    # Verificandos se a consulta SQL foi executada corretamente
    mock_cursor.execute.assert_any_call("SELECT * FROM imoveis WHERE id = %s", (1,))
    mock_cursor.execute.assert_any_call("DELETE FROM imoveis WHERE id = %s", (1,))
    mock_conn.commit.assert_called_once()
    mock_conn.close.assert_called_once()
    
    
@patch("servidor.connect_db")
def test_del_imovel_nao_encontrado(mock_connect_db, client):
    # Criandos um Mock para a conexão e o cursor
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    
    # Configurandos o Mock para retornar o cursor quando chamarmos conn.cursor()
    mock_conn.cursor.return_value = mock_cursor

    # Substituíndo a função `connect_db` para retornar nosso Mock em vez de uma conexão real
    mock_connect_db.return_value = mock_conn

    # Simula o banco retornando vazio
    mock_cursor.fetchone.return_value = None
    
    # Fazendo requisição para a api
    response = client.delete("/imoveis/999")
    
    # verificando se o código de status retornou 404
    assert response.status_code == 404
    assert response.get_json() == {"erro": "Imóvel não encontrado"}

    # Verificando se a consulta de busca foi executada
    mock_cursor.execute.assert_called_once_with("SELECT * FROM imoveis WHERE id = %s", (999,))
    
    # Verificando que não houve commit
    mock_conn.commit.assert_not_called()
    
@patch("servidor.connect_db")
def test_del_imovel_erro_conexao(mock_connect_db, client):
    # Simula erro de conexão
    mock_connect_db.return_value = None

    # Fazendo requisição para a api
    response = client.delete("/imoveis/1")

    # verificando se o código de status retornou 500
    assert response.status_code == 500
    assert response.get_json() == {"erro": "Erro ao conectar ao banco de dados"}