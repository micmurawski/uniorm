#
# Configuration
#

PROJECT_NAME = uniorm

include build/makefile/root.mk
include build/makefile/python.mk
include build/makefile/lint.mk
include build/makefile/githooks.mk

.PHONY: project_name
project_name:
	@echo -n $(PROJECT_NAME)

