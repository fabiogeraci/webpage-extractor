webpage-extractor/
├── app/
│ ├── __init__.py
│ ├── main.py
│ ├── containers.py
│ ├── config.py
│ ├── domain/
│ │ ├── __init__.py
│ │ ├── ports.py
│ │ ├── models.py
│ ├── infrastructure/
│ │ ├── __init__.py
│ │ ├── http/
│ │ │ ├── __init__.py
│ │ │ └── httpx_client.py
│ │ ├── extraction/
│ │ │ ├── __init__.py
│ │ │ ├── trafilatura_markdown_extractor.py
│ │ │ └── image_extractor.py
│ │ └── storage/
│ │ ├── __init__.py
│ │ └── filesystem_storage.py
│ ├── application/
│ │ ├── __init__.py
│ │ └── extract_usecase.py
│ └── presentation/
│ ├── __init__.py
│ ├── api.py
│ └── templates/
│ ├── base.html
│ └── index.html
├── tests/
│ ├── __init__.py
│ └── test_extract_usecase.py
├── pyproject.toml
├── uv.lock # optional (if you decide to use uv to lock)
├── Dockerfile
├── docker-compose.yml
└── README.md