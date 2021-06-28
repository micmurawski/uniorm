.PHONY: install_githooks
install_githooks:
	cp build/makefile/githooks/prepare-commit-msg .git/hooks/prepare-commit-msg
	cat build/makefile/githooks/prepare-commit-msg > .git/hooks/prepare-commit-msg