PYTHON_CMD ?= python3

.PHONY: build
build:
	rm -rf out/*
	${PYTHON_CMD} -m website
	cp -r website/static out
	cp -r laserkukkahattu out

.PHONY: install
install:
	@echo do install

.PHONY: dev
dev:
	@cd out && ${PYTHON_CMD} -m http.server 8080
