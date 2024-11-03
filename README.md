# pypcr
Configuration registry for VOIP endpoints. This makes it possible to automatically provision device like
hardware/software phones automatically.

## Deployment
A Docker image is provided for deploying. Everything is configured through environment variables. Important
ones are:

- `SECRET_KEY`: required by Django
- `ALLOWED_HOSTS`: hosts that the server will be accessed from
- `CSRF_TRUSTED_ORIGINS`: required to log in to the admin interface (don't forget to include protocol)
- `DB_*`: used to set up a connection to PostgreSQL

With a properly configured container, then the migrations need to be run and static files generated and served
accordingly (usually through a proxy like Nginx or Caddy).
