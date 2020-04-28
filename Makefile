BIN=venv/bin/

venv: activate

activate: requirements.txt
	test -d venv || virtualenv venv
	. $(BIN)activate; pip install -Ur requirements.txt
	touch $(BIN)activate

test: venv
	. $(BIN)activate; nosetests project/test

clean:
	rm -rf venv
	find -iname "*.pyc" -delete

nvenv:
	python3 -m venv venv

install:	
	$(BIN)pip install -r requirements.txt

install3:	
	$(BIN)pip install -r requirements-python3.txt

run:
	$(BIN)python main.py

freeze:
	pip3 freeze > requirements.txt

freeze3:
	pip3 freeze > requirements-python3.txt