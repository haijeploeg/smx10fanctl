.PHONY: clean virtualenv

clean:
	find . -name '*.py[co]' -delete

virtualenv:
	python3 -m venv env
	env/bin/pip install wheel pylint cement==3.0.4
	env/bin/pip install -e .
	env/bin/python setup.py develop
	@echo
	@echo "VirtualENV Setup Complete. Now run: source env/bin/activate"
	@echo
