run:
	python3 ./src/

test:
	python3 -m unittest discover -v src

install:
	git submodule update --init --recursive
	python3 -m pip install -r requirements.txt
	python3 -m pip install pylint
	rm -rf ./build/

clean:
	rm -rf ./build/

.PHONY: build
build:
	docker build -t canary:dev .

dev: build
	docker run canary-dev

lint:
	pylint --disable=all \
		--enable=unused-argument \
		--enable=global-statement \
		--enable=global-variable-not-assigned \
		--enable=used-before-assignment \
		--enable=function-redefined \
		--enable=abstract-class-instantiated \
		--enable=invalid-unary-operand-type \
		--enable=no-member \
		--enable=undefined-variable \
		--enable=undefined-loop-variable ./src