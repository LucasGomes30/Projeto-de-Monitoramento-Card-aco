Requisitos Mínimos para Utilização do Projeto de Monitoramento Cardíaco
=====================================================================

Tecnologias Utilizadas
----------------------

Linguagens e Frameworks:
- Python 3.8+: Linguagem de programação principal.
- Flask: Framework web para desenvolvimento do servidor backend.

Bibliotecas Python:
- Flask-SQLAlchemy: Integração do SQLAlchemy com Flask para manipulação de banco de dados.
- Flask-Migrate: Gerenciamento de migrações de banco de dados com Alembic.
- Flask-Login: Gerenciamento de sessão de usuários.
- Flask-Mail: Envio de e-mails para funcionalidades como confirmação de registro.
- Pandas: Manipulação e análise de dados.
- Matplotlib: Geração de gráficos.
- Werkzeug: Utilitários para WSGI, manipulação de senhas.
- Itsdangerous: Geração de tokens seguros para confirmação de e-mail.

Banco de Dados:
- MySQL: Sistema de gerenciamento de banco de dados relacional utilizado para armazenar informações de usuários e dados de monitoramento.

Hardware Utilizado:
- Xiaomi Mi Band 4: Dispositivo vestível utilizado para monitorar a frequência cardíaca dos pacientes.
- Aplicativo Zepp Life (anteriormente conhecido como Mi Fit): Aplicativo utilizado para sincronizar dados da Xiaomi Mi Band 4 com o dispositivo móvel e exportar os dados de frequência cardíaca.

Outras Tecnologias:
- SMTP: Protocolo utilizado para envio de e-mails de confirmação de registro. Configurado para usar o serviço do Gmail.

Requisitos de Hardware e Software
---------------------------------
- Processador: Mínimo de 2 GHz dual-core.
- Memória RAM: Mínimo de 2 GB.
- Espaço em Disco: Mínimo de 10 GB de espaço disponível.
- Sistema Operacional: Windows, macOS ou Linux.

Dispositivo Móvel:
- Dispositivo: Smartphone com Android ou iOS compatível com Xiaomi Mi Band 4.
- Aplicativo: Zepp Life instalado e configurado para sincronizar com a Xiaomi Mi Band 4.

Software:
- Python 3.8+: Instalado no servidor/computador.
- MySQL: Instalado e configurado no servidor/computador.
- Bibliotecas Python: Instaladas via pip conforme especificado no arquivo requirements.txt.

Instalação de Dependências
--------------------------
Certifique-se de que todas as dependências necessárias estão instaladas. Isso pode ser feito utilizando o seguinte comando após ativar o ambiente virtual do Python:
pip install -r requirements.txt


Requirements
------------------------
Flask==2.0.2
Flask-SQLAlchemy==2.5.1
Flask-Migrate==3.1.0
Flask-Login==0.5.0
Flask-Mail==0.9.1
pandas==1.3.4
matplotlib==3.4.3
itsdangerous==2.0.1
Werkzeug==2.0.2



Configuração do Banco de Dados
------------------------------
1. Crie um banco de dados MySQL chamado `monitoramento_pacientes` e configure as credenciais no arquivo `flasktest.py`:
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://USERNAME
@localhost/monitoramento_pacientes'


2. Execute as migrações para configurar o esquema inicial do banco de dados:
flask db init
flask db migrate -m "Initial migration."
flask db upgrade



Exportação de Dados
-------------------
Os dados de frequência cardíaca devem ser exportados do aplicativo Zepp Life e salvos no formato JSON. Certifique-se de que o arquivo está no local correto e que o caminho está configurado no código:
df = pd.read_json("C:\Users\ruang\Desktop\curso_python3\heartrate_auto.json")



Configuração de E-mail
----------------------
Configure as credenciais de e-mail no arquivo `flasktest.py` para permitir o envio de e-mails de confirmação:
app.config['MAIL_USERNAME'] = 'monitoramentocardiaco1@gmail.com'
app.config['MAIL_PASSWORD'] = 'rwcs wupf jplb jsmu'


Execução do Projeto
-------------------
Para iniciar o servidor, execute o seguinte comando:
python flasktest.py


A aplicação estará disponível em `http://127.0.0.1:8080`.
