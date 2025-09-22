.PHONY: install run test docker-build docker-run clean

install:
	python -m venv venv
	venv/bin/pip install --upgrade pip
	venv/bin/pip install -r requirements.txt

run:
	venv/bin/python -m src.main

test:
	venv/bin/pytest tests/

docker-build:
	docker build -t peer-skill-exchange .

docker-run:
	docker run -it --rm peer-skill-exchange venv/bin/python -m src.main

clean:
	rm -rf venv __pycache__ *.pyc *.pyo
