FROM ghcr.io/astral-sh/uv:python3.12-alpine AS builder

RUN apk add gcc libpq-dev musl-dev;

WORKDIR /app

COPY . .

RUN uv sync --extra=production --frozen --no-install-project --no-dev;

FROM python:3.12-alpine3.19

RUN apk add libpq-dev;

WORKDIR app

COPY --from=builder /app .

ENV PATH="/app/.venv/bin:$PATH"

ENV STATIC_ROOT=/static

ENV PYTHONPATH=/app/src:$PYTHON_PATH

ENV DJANGO_SETTINGS_MODULE=pypcr.settings

ENV DEBUG=False

EXPOSE 8000

ENTRYPOINT ["gunicorn", "pypcr.wsgi"]

CMD ["-b", "0.0.0.0:8000"]
