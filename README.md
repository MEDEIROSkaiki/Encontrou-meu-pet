# 🐾 Encontrou Meu Pet

Aplicação web para cadastro, pesquisa e anúncio de animais, com foco em facilitar o encontro entre pets perdidos e seus tutores ou novos adotantes. Desenvolvido em **Python (Flask)** com conexão a banco de dados via **ODBC**.

---

## 🚀 Funcionalidades

- Tela de login e cadastro de usuário
- Validação de e-mail e senha no cadastro
- Formulário para cadastro de animais (espécie, raça, porte, gênero, situação)
- Consulta dinâmica de espécies, raças e atributos relacionados
- APIs REST para retorno de dados ao frontend
- Páginas renderizadas com templates HTML (via `render_template`)

---

## 🧱 Estrutura do Projeto

```bash
.
├── app.py                     # Arquivo principal que inicia a aplicação
├── .env                       # Variáveis de ambiente (não versionado)
├── .gitignore                 # Ignora arquivos para versionamento Git
├── README.md                  # Documentação do projeto
├── requirements.txt           # Dependências do projeto
├── dev-requirements.in        # Dependências de desenvolvimento
├── dev-requirements.txt       # Dependências resolvidas de dev
├── requirements.in            # Dependências base
│
├── db/                        # Camada de acesso ao banco de dados
│   ├── __init__.py
│   ├── dicionarios_db.py
│   ├── usuario_db.py
│   └── __pycache__/           # Cache dos arquivos compilados
│       ├── especies_db.cpython-313.pyc
│       ├── generos_db.cpython-313.pyc
│       ├── portes_db.cpython-313.pyc
│       ├── racas_db.cpython-313.pyc
│       ├── situacoes_db.cpython-313.pyc
│       └── usuario_db.cpython-313.pyc
│
├── rotas/                     # Arquivos que definem as rotas da aplicação
│   ├── __init__.py
│   ├── api.py
│   ├── auth.py
│   └── main.py
│
├── static/                    # Arquivos estáticos (CSS, JS, imagens)
│   ├── css/
│   │   ├── cadastro.css
│   │   ├── cadastro_2.css
│   │   ├── cadastro_3.css
│   │   ├── cadastro_concluido.css
│   │   ├── cadastro_usuario.css
│   │   ├── login.css
│   │   ├── pesquisa.css
│   │   └── style.css
│   ├── img/                   # (Pasta de imagens)
│   └── js/
│       ├── cadastro_2.js
│       └── cadastro_usuario.js
│
├── templates/                 # Templates HTML para renderização
│   ├── cadastro/
│   │   ├── cadastro.html
│   │   ├── cadastro_2.html
│   │   ├── cadastro_3.html
│   │   ├── cadastro_concluido.html
│   │   └── cadastro_usuario.html
│   ├── index.html
│   ├── login.html
│   └── pesquisa.html
│
├── utils/                     # Funções utilitárias
│   ├── __pycache__/
│   │   ├── with_connection.cpython-313.pyc
│   ├── login_verification.py
│   └── with_connection.py
│
└── venv/                      # Ambiente virtual Python (não versionado)
    ├── Include/
    ├── Lib/
    │   └── site-packages/
    ├── Scripts/
    └── pyvenv.cfg

```

---

## 🛠️ Como executar

### Pré-requisitos

- Python 3.13+
- Driver ODBC instalado (ex: para SQL Server)

### 1. Instalar as dependências

```bash
bash
CopiarEditar
pip install -r requirements.txt

```

### 2. Configurar variáveis de ambiente

Crie um arquivo `.env` com as seguintes variáveis:

```
ini
CopiarEditar
DRIVER={SQL Server}
SERVER=seu_servidor
DATABASE=seu_banco
UID=usuario
PWD=senha
```

### 3. Executar o servidor

```bash
bash
CopiarEditar
python app.py
```

Acesse [http://localhost:5000](http://localhost:5000/) no navegador.

---

## 🧪 Rotas Principais

| Método | Rota | Descrição |
| --- | --- | --- |
| GET | `/` | Página inicial |
| GET | `/login` | Página de login |
| GET | `/cadastrar` | Página de cadastro |
| POST | `/cadastrar` | Cadastro de usuário |
| GET | `/pesquisa` | Página de pesquisa |
| GET | `/anunciar/cadastro` | Página de cadastro de animal |
| GET | `/anunciar/get_all_especies` | Retorna lista de espécies |
| GET | `/anunciar/get_all_generos` | Retorna lista de gêneros |
| GET | `/anunciar/get_all_portes` | Retorna lista de portes |
| GET | `/anunciar/get_all_situacoes` | Retorna lista de situações |
| POST | `/racas` | Retorna raças com base na espécie |

---

## 📦 Dependências Principais

- Flask
- [pyodbc](https://pypi.org/project/pyodbc/)
- [python-dotenv](https://pypi.org/project/python-dotenv/)

---

## 📁 .gitignore

O projeto ignora:

- Arquivos temporários e cache (`__pycache__`, `.pyc`)
- Configurações do VS Code (`.vscode`)
- Arquivos `.env` com dados sensíveis

---

## 👨‍💻 Autores

- Ronaldo Moreira
    - [Romope83](https://github.com/Romope83)
- Kaiki Medeiros
    - GitHub: [MEDEIROSkaiki](https://github.com/MEDEIROSkaiki)
- Kaua Felipe de Melo
    - GitHub: [Drivol](https://github.com/Drivol)
- Felipe Oliveira
    - GitHub: [feolcostaa](https://github.com/feolcostaa)

---

## 🔗 Links

https://www.figma.com/design/vLqg0Rf4S8QSEaVj1wzENh/Untitled?node-id=0-1&t=YIBUMzBAihjUTdfH-1

https://trello.com/invite/b/6837a2c44ac0b4c93fc71ccf/ATTIbb34e870aa5927287c0ac465000a2310435C03C9/projeto-fim-semestre

---

## 📄Regras de Negócio

[Regras de Negócio](https://www.notion.so/Regras-de-Neg-cio-214cd7be416f806cb98cfeb5d4bf6320?pvs=21)
