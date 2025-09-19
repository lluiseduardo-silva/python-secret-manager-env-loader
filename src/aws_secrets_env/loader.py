import json
import os

import boto3


def load_secrets(secret_names: list[str]) -> None:
    """
    Carrega segredos do AWS Secrets Manager e injeta no os.environ.

    - Se o segredo for JSON, cada chave vira uma variável de ambiente (em MAIÚSCULO).
    - Se o segredo for string simples, vira uma variável com o nome do segredo (em MAIÚSCULO).
    """
    client = boto3.client("secretsmanager")

    for secret_name in secret_names:
        response = client.get_secret_value(SecretId=secret_name)
        secret_string = response.get("SecretString")
        if not secret_string:
            continue

        try:
            secret_map = json.loads(secret_string)
            if isinstance(secret_map, dict):
                for k, v in secret_map.items():
                    os.environ[k.upper()] = str(v)
            else:
                os.environ[secret_name.upper()] = str(secret_map)
        except json.JSONDecodeError:
            os.environ[secret_name.upper()] = secret_string
