# Setup local

1. Crie o ambiente:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

2. Configure o ambiente:

```bash
cp .env.example .env
```

3. Crie o banco Postgres:

```sql
CREATE USER smart_system WITH PASSWORD 'smart_system_password';
CREATE DATABASE smart_system_base OWNER smart_system;
```

4. Rode migrations e seed:

```bash
python manage.py migrate
python manage.py seed_base
```

5. Acesse:

- Admin: http://127.0.0.1:8000/admin/
- API: http://127.0.0.1:8000/api/v1/health/

Usuário inicial criado pelo seed:

- login: `admin`
- senha: `admin123`

Troque a senha em produção. Sem choro: senha padrão em produção é convite para desastre.
