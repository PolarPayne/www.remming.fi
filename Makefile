PYTHON_CMD ?= python3

.PHONY: build
build:
	rm -rf out/*
	${PYTHON_CMD} -m website
	cp -r website/static out
	cp -r laserkukkahattu out

.PHONY: install
install: guard-LOCATION build
	cp -r out/* ${LOCATION}

.PHONY: dev
dev:
	@cd out && ${PYTHON_CMD} -m http.server 8080

.PHONY: guard-%
guard-%:
	@if [ "${${*}}" = "" ]; then \
	echo "Environment variable $* not set"; \
	exit 1; \
	fi
