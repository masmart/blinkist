# Seed data

Database structure belongs exclusively to Alembic migrations. The seed command
contains only optional, idempotent development data and can be run repeatedly.

```powershell
python -m flask --app app db upgrade
python -m seeds.seed
```

`public.sql` is retained temporarily as a legacy content snapshot. It must not
be used to create or upgrade the database schema and can be removed after its
content has been migrated to purpose-built import fixtures.
