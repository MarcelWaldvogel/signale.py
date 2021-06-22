python-package wheel:
	${RM} -rf dist/* build/*
	./setup.py sdist bdist_wheel

pypi:	python-package
	twine upload dist/*
