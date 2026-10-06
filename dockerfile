FROM python:3.11-slim-bookworm

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

RUN apt-get update && apt-get install -y --no-install-recommends \
    fonts-dejavu-core \
    libharfbuzz-subset0 \
    libpango-1.0-0 \
    libpangoft2-1.0-0 \
    && rm -rf /var/lib/apt/lists/*

RUN useradd --create-home --uid 10001 app \
    && mkdir -p /app \
    && chown app:app /app

WORKDIR /app
COPY requirements.txt .
RUN python -m pip install -r requirements.txt

COPY --chown=app:app . .
RUN sed -i 's/\r$//' start.sh build.sh \
    && chmod +x start.sh build.sh \
    && mkdir -p staticfiles proyectoWeb/media \
    && chown app:app staticfiles proyectoWeb/media

USER app
EXPOSE 8000
CMD ["sh", "./start.sh"]
