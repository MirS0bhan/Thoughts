.PHONY: generate-deps

generate-deps:
	uv run flatpak-pip-generator --requirements-file='./requirements.txt' -o pypi-dependencies.json --runtime='org.freedesktop.Sdk//24.08'

pot:
	scripts/update-po.sh
