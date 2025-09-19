# aws-secrets-env

Um pacote Python para buscar segredos no AWS Secrets Manager e injetá-los de forma segura em variáveis de ambiente (`os.environ`). Ideal para aplicações 12-factor que consomem configuração via env vars.

## Sumário

- Recursos
- Requisitos
- Instalação (via Git)
- Conceitos de uso
- Exemplos de uso
- Formatos de segredo suportados
- Permissões IAM mínimas
- Variáveis de ambiente reconhecidas
- Boas práticas e observações
- Solução de problemas (FAQ)
- Desenvolvimento
- Licença

## Recursos

- Carrega um segredo do AWS Secrets Manager por nome ou ARN.
- Injeta pares chave-valor no `os.environ` da aplicação.
- Suporte a segredos em JSON (chave-valor) e string simples.
- Prefixo opcional para nomes de variáveis (ex.: `MYAPP_`).
- Política de sobrescrita configurável (não sobrescrever por padrão).
- Integração com credenciais padrão da AWS (perfil, variáveis de ambiente, EC2/ECS/Role, SSO).

## Requisitos

- Python 3.9+.
- Dependências: `boto3`.
- Credenciais da AWS válidas no ambiente (perfil local, variáveis, ou cargo/role).

## Instalação (via Git)

Este pacote ainda não está publicado no PyPI. Instale diretamente do Git:

- Instalação a partir do branch principal (substitua pela URL do seu repositório):

````bash
bash pip install "git+https://github.com/lluiseduardo-silva/python-secret-manager-env-loader.git#egg=aws-secrets-env"
````

- Instalação fixando uma tag/versão específica:

````bash
bash pip install "git+https://github.com/lluiseduardo-silva/python-secret-manager-env-loader.git@v0.1.0#egg=aws-secrets-env"
````

Dica: para ambientes reprodutíveis, prefira instalar por tag ou commit.
## Desenvolvimento

- Requisitos locais:
  - Python 3.9+
  - virtualenv
- Passos:
  ```bash
  git clone https://github.com/lluiseduardo-silva/python-secret-manager-env-loader.git
  cd python-secret-manager-env-loader
  ```
#### Crie e ative um ambiente virtual
````bash
  python -m virtualenv .venv
  . .venv/bin/activate  # no Windows: .venv\Scripts\activate
````
#### Instale em modo desenvolvimento
````bash
  
  pip install -e ".[dev]"
````

#### Rode testes
````bash
  pytest -q
````

- Estilo de código: `pylint`, `pyflakes`, `mypy` (se aplicável).
- Cobertura: `coverage run -m pytest && coverage html`

## Licença

Defina a licença do projeto (ex.: MIT, Apache-2.0) e inclua o arquivo `LICENSE`.

—
Dúvidas, sugestões ou problemas? Abra uma issue no repositório.

## Scrip testa e roda no sonarqube

### Precisa ter um token definido na variavel de ambiente do terminal chamdo de SQTOKEN
````powershell
$env:SQTOKEN = "sqn_XXXXXXX"
````

### Roda o script (vai executar um pip install -e .[dev,security] antes de executar as analises)
````powershell
.\generate_reports.ps1
````