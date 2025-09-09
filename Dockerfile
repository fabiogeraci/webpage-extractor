# Python 3.11 slim base
FROM python:3.11-slim


ENV PYTHONDONTWRITEBYTECODE=1 \
PYTHONUNBUFFERED=1 \
PIP_NO_CACHE_DIR=1


# System deps
RUN apt-get update && apt-get install -y --no-install-recommends \
build-essential \
libjpeg-dev zlib1g-dev \
ca-certificates \
&& rm -rf /var/lib/apt/lists/*


WORKDIR /app


COPY pyproject.toml ./
RUN pip install --upgrade pip && pip install -e .


COPY app ./app
COPY README.md ./


EXPOSE 8000


CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]