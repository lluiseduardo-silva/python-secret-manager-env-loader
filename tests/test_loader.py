import copy
import json
import os
from unittest.mock import patch, MagicMock

import pytest
from botocore.exceptions import ClientError

from aws_secrets_env import load_secrets


@pytest.fixture(autouse=True)
def restore_env():
    original_env = copy.deepcopy(os.environ)
    yield
    os.environ.clear()
    os.environ.update(original_env)


@patch("boto3.client")
def test_load_json_secret(mock_boto):
    # Mocka resposta do boto3
    mock_client = MagicMock()
    mock_client.get_secret_value.return_value = {
        "SecretString": json.dumps({"dbhost": "localhost", "dbuser": "admin"})
    }
    mock_boto.return_value = mock_client

    load_secrets(["rds"])

    assert os.environ["DBHOST"] == "localhost"
    assert os.environ["DBUSER"] == "admin"
    # não deve criar "RDS" porque era JSON
    assert "RDS" not in os.environ


@patch("boto3.client")
def test_load_string_secret(mock_boto):
    mock_client = MagicMock()
    mock_client.get_secret_value.return_value = {"SecretString": "supersecret"}
    mock_boto.return_value = mock_client

    load_secrets(["gpt-rag"])

    assert os.environ["GPT-RAG".upper()] == "supersecret"


@patch("boto3.client")
def test_load_invalid_json_secret(mock_boto):
    mock_client = MagicMock()
    # Segredo não é JSON válido
    mock_client.get_secret_value.return_value = {"SecretString": "{not_json"}
    mock_boto.return_value = mock_client

    load_secrets(["broken-secret"])

    # Deve cair no except e injetar a string crua
    assert os.environ["BROKEN-SECRET".upper()] == "{not_json"


@patch("boto3.client")
def test_load_non_string_secret(mock_boto):
    mock_client = MagicMock()
    # Simula um segredo sem SecretString
    mock_client.get_secret_value.return_value = {}
    mock_boto.return_value = mock_client

    load_secrets(["empty-secret"])

    # Não deve injetar nada
    assert "EMPTY-SECRET" not in os.environ


@patch("boto3.client")
def test_load_json_secret_not_dict(mock_boto):
    mock_client = MagicMock()
    # Segredo é JSON válido, mas não é dict → cai no else
    mock_client.get_secret_value.return_value = {"SecretString": json.dumps(["val1", "val2"])}
    mock_boto.return_value = mock_client

    load_secrets(["array-secret"])

    # Deve salvar o JSON serializado inteiro na variável com nome do segredo
    assert os.environ["ARRAY-SECRET"] == "['val1', 'val2']" or os.environ["ARRAY-SECRET"] == '["val1", "val2"]'


@patch("boto3.client")
def test_boto3_clienterror(mock_boto):
    # Simula erro do Secrets Manager
    mock_client = MagicMock()
    mock_client.get_secret_value.side_effect = ClientError(
        error_response={"Error": {"Code": "ResourceNotFoundException", "Message": "Secret not found"}},
        operation_name="GetSecretValue"
    )
    mock_boto.return_value = mock_client

    # Deve levantar a exceção para o chamador (não engolimos ClientError)
    import pytest
    with pytest.raises(ClientError):
        load_secrets(["not-exist"])


@patch("boto3.client")
def test_load_empty_string_secret(mock_boto):
    mock_client = MagicMock()
    mock_client.get_secret_value.return_value = {"SecretString": ""}
    mock_boto.return_value = mock_client

    load_secrets(["empty-string"])

    # Não deve criar variável nenhuma
    assert "EMPTY-STRING" not in os.environ


@patch("boto3.client")
def test_load_json_with_non_string_values(mock_boto):
    mock_client = MagicMock()
    mock_client.get_secret_value.return_value = {
        "SecretString": json.dumps({"port": 5432, "enabled": True, "desc": None})
    }
    mock_boto.return_value = mock_client

    load_secrets(["rds-extra"])

    # Todos devem ser convertidos para string
    assert os.environ["PORT"] == "5432"
    assert os.environ["ENABLED"] == "True"
    assert os.environ["DESC"] == "None"
