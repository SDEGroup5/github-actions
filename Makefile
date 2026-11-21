.PHONY: init clean

init:
	git config core.hooksPath .githooks
	python3 -m venv .venv
	.venv/bin/pip install poetry yapf pylint ruff
#	.venv/bin/pip install -r requirements.txt

deactivate:
	git config --unset-all --local core.hooksPath

clean:
	rm -r */*/__pycache__ */*/*/__pycache__
