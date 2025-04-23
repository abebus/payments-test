# Stage 1: Builder
FROM python:3.13-alpine AS builder

WORKDIR /app

# RUN apk add --no-cache build-base libffi-dev

RUN pip install --upgrade pip && pip install uv

COPY . .

RUN uv pip compile pyproject.toml > requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

RUN python manage.py collectstatic --noinput


# Stage 2: Final
FROM python:3.13-alpine

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# RUN apk add --no-cache libffi
COPY --from=builder /usr/local /usr/local

WORKDIR /app

COPY --from=builder /app /app

COPY gunicorn.sh /gunicorn.sh
RUN chmod +x /gunicorn.sh

CMD ["/gunicorn.sh"]
