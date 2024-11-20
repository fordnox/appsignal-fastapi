#!make

# Make sure you have .env file in root directory
include .env
export

all: install run

install:
	uv sync --extra dev

run:
	uv run fastapi dev

run-ot:
	uv run fastapi dev open.py

run-os:
	uv run fastapi dev os-exporter.py

lint:
	uv run ruff format .
	uv run ruff check --fix  .
	uv run ruff check --select I --fix .

