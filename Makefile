dev:
	FLASK_ENV=devel PORT=55123 python app.py

lint:
	pylint app.py utils.py

test:
	pytest -vv
