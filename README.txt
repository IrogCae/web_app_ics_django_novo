web_app_ics_django/
├── .venv/                        # seu virtualenv
├── .gitignore
├── requirements.txt
├── .env                          # variáveis de ambiente (SECRET_KEY, DEBUG, …)
├── manage.py
├── core/                         # seu “project” Django
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── accounts/                     # app de autenticação
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── migrations/
│   ├── models.py
│   ├── tests.py
│   ├── urls.py
│   ├── views.py
│   └── templates/
│       └── accounts/
│           └── login.html
├── ics_app/                      # seu dashboard / lógica principal
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── urls.py
│   ├── views.py
│   ├── utils/                    # funções auxiliares
│   │   ├── __init__.py
│   │   └── data_processing.py
│   ├── management/               # comando para ingestão diária
│   │   └── commands/
│   │       └── update_dados_iniciativas.py
│   ├── static/
│   │   └── ics_app/
│   │       ├── css/
│   │       ├── js/
│   │       └── images/
│   └── templates/
│       └── ics_app/
│           ├── base.html
│           ├── home.html
│           ├── iniciativas.html
│           ├── pleitos_dash.html
│           ├── projetos_dash.html
│           └── visao-geral.html
└── data/                         # branch “raw data” fora do git
    └── dados_concatenados.xlsx
