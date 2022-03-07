run:
	python3 ./

test:
	python3 -m unittest discover -v src

install:
	git submodules update --init --recursive
	python3 -m pip install -r requirements.txt