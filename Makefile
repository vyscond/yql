env=env
python=$(env)/bin/python
pip=$(env)/bin/pip

requirements:
	$(pip) freeze > requirements.txt

test:
	$(python) test.py
	