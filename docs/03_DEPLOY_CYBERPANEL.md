# Deploy em VPS HostGator com CyberPanel

Fluxo recomendado:

1. Criar site no CyberPanel.
2. Criar banco PostgreSQL ou instalar/usar Postgres no servidor.
3. Subir o projeto para `/home/<dominio>/smart_system_base`.
4. Criar `.env` com settings de produção.
5. Instalar dependências em `.venv`.
6. Rodar:

```bash
source .venv/bin/activate
python manage.py migrate
python manage.py collectstatic --noinput
python manage.py check --deploy
```

7. Criar serviço systemd Gunicorn:

```ini
[Unit]
Description=Smart System Base Gunicorn
After=network.target

[Service]
User=<usuario>
Group=<usuario>
WorkingDirectory=/home/<dominio>/smart_system_base
Environment="DJANGO_SETTINGS_MODULE=config.settings.prod"
ExecStart=/home/<dominio>/smart_system_base/.venv/bin/gunicorn config.wsgi:application --bind 127.0.0.1:8001 --workers 3
Restart=always

[Install]
WantedBy=multi-user.target
```

8. Configurar OpenLiteSpeed como reverse proxy para `127.0.0.1:8001`.

9. Ativar SSL no CyberPanel.

10. Rodar `python manage.py check --deploy` antes de publicar.
