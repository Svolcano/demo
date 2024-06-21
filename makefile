run:
	uvicorn main:app --host '127.0.0.1' --port 8000 --reload

py_target=database models tools main.py settings.py

format:
	isort $(py_target)
	black $(py_target)

test:
	pytest -v .

update_r:
	pip freeze > requirements.txt

clean:
	find . -name "__pycache__" -exec rm -rf {} \+
	rm -rf .pytest_cache

check:
	pyflakes $(py_target)
