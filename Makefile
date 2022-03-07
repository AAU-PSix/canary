run:
	python3 ./

test:
	python3 -m unittest discover -v src

install:
	python3 -m pip install --user canary-env

inspect-js:
	nm -D nm -D ./canary-env/lib/python3.9/site-packages/tree_sitter/binding.cpython-39-x86_64-linux-gnu.so