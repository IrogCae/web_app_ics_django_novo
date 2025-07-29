@echo off
REM — Navega para a pasta do script (diretório onde está este .bat)
cd /d %~dp0

REM — Configura variáveis para acompanhamento de progresso
setlocal enabledelayedexpansion
set total=4
set count=0
set errors=0

REM — Ativa o virtualenv
call .\.venv\Scripts\activate.bat


REM — Roda o comando Django

python manage.py update_dados_pedidos_adiantados
python manage.py update_dados_pedidos_aq
python manage.py update_dados_pedidos_pagos
python manage.py update_dados_pedidos_pendentes
python manage.py update_dados_pedidos
python manage.py update_dados_pleitos
python manage.py update_dados_projetos_iniciativas
python manage.py update_dados_projetos
python manage.py update_rda_sem_pedido

REM — (Opcional) Grava log
if not exist logs mkdir logs
echo %DATE% %TIME% - update concluído >> logs\update.log
