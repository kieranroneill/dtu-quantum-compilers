SHELL := /bin/bash

all: install

install:
		@echo ">>> Installing dependencies"
		python3 -m venv .venv
		source .venv/bin/activate && \
				pip install -r requirements.txt && \
				pip install -e . && \
				deactivate

run:
		@echo ">>> Running main.py"
		python3 -m venv .venv
		source .venv/bin/activate && \
				python3 main.py

test:
		@echo ">>> Running unit tests"
		python3 -m venv .venv
		source .venv/bin/activate && \
				python3 -m pytest -vv
