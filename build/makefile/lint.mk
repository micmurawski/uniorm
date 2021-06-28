test: swagger_lint
lint: swagger_lint

.PHONY: swagger_lint
swagger_lint: $(PYTHON_VENV)
ifneq ($(SWAGGER_FILE_DIR), "")
	$(call in_venv,$(PIP) install PyYAML)
	$(call in_venv,$(PYTHON) -c "import yaml;import sys;yaml.safe_load(sys.stdin)" < $(SWAGGER_FILE_DIR))
else
	@echo "missing SWAGGER_FILE_DIR"
endif
