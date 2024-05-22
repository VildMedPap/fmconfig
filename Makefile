.DEFAULT_GOAL := help

# Virtual environment paths
VIRTUAL_ENV_NAME := .venv
TOOLS_FIRST_INSTALLED := $(VIRTUAL_ENV_NAME)/.tools_first_installed

# Directories
ROOT_DIR := $(CURDIR)
CACHE_DIR := $(ROOT_DIR)/.cache
BIN_DIR := $(ROOT_DIR)/bin
PKG_DIR := $(ROOT_DIR)/src
TEST_DIR := $(ROOT_DIR)/tests

#------------------#
#   MISC TARGETS   #
#------------------#

.PHONY: help %

help:
	@$(BIN_DIR)/help.sh "$(MAKEFILE_LIST)"

%:
	@echo "Target $@ is not defined. Running help target instead:\n"
	@$(MAKE)

#----------------------#
#   TEARDOWN TARGETS   #
#----------------------#

.PHONY: teardown rm-venv rm-cache

teardown: rm-venv rm-cache ## Remove .venv, .cache, etc.

rm-venv:
	@rm -rf $(VIRTUAL_ENV_NAME)

rm-cache:
	@rm -rf $(CACHE_DIR)

#----------------#
#   CI TARGETS   #
#----------------#

.PHONY: ci linting test

ci: linting test ## Emulate CI pipeline (linters and tests)

test: ## Run test suite
	@poetry run pytest $(TEST_DIR) --suppress-no-test-exit-code

#---------------------#
#   LINTERS TARGETS   #
#---------------------#

.PHONY: linting ruff mypy check-packages shellcheck

linting: ruff mypy check-packages shellcheck ## Run all linters

ruff:
	@poetry run ruff check --config ${ROOT_DIR}/pyproject.toml --no-fix $(PKG_DIR)

mypy:
	@poetry run mypy $(PKG_DIR)

check-packages:
	@poetry check
	@poetry run pip check
	@poetry export -f requirements.txt --without-hashes --with dev,test | poetry run safety check --full-report --stdin

shellcheck:
	@$(eval SH_FILES := $(shell find . -name '*.sh' -not -path '*/.*'))
	@$(if $(SH_FILES),poetry run shellcheck $(SH_FILES), @echo "No shell files found")

#------------------------#
#   FORMATTERS TARGETS   #
#------------------------#

.PHONY: formatting ruff-format

formatting: ruff-format ## Run all formatters

ruff-format:
	@poetry run ruff format --config ${ROOT_DIR}/pyproject.toml $(PKG_DIR)
	@poetry run ruff check --config ${ROOT_DIR}/pyproject.toml --fix-only $(PKG_DIR)

#-------------------#
#   SETUP TARGETS   #
#-------------------#

.PHONY: install create-environment install-dependencies

install: create-environment $(TOOLS_FIRST_INSTALLED) install-dependencies ## Setup environment and install all dependencies

$(TOOLS_FIRST_INSTALLED):
	@touch $@

create-environment:
	@pyenv install --skip-existing $(shell cat $(ROOT_DIR)/.python-version)
	@poetry env use -- $(shell pyenv which python)

install-dependencies:
	@poetry install --with dev,test
