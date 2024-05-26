.PHONY: build test run

run: build
	@docker run --rm --network=league-of-data_default roqueando/app:stable $(module)

build:
	@docker build -t roqueando/app:stable -f Dockerfile .

test-spec:
	python -m pytest -s -v -k $(spec)

test:
	python -m pytest -s -v
