run:
	python3 ./src/

test:
	python3 -m unittest discover -v src

install:
	git submodule update --init --recursive
	python3 -m pip install -r requirements.txt
	rm -rf ./build/

clean:
	rm -rf ./build/