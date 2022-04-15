.PHONY: run
run:
	python3 ./src/

.PHONY: test
test: lint
	rm -rf ./graphs/
	python3 -m unittest discover -v src

.PHONY: test-fast
test-fast:
	rm -rf ./graphs/
	python3 -m unittest discover -v src

.PHONY: install
install:
	git submodule update --init --recursive
	python3 -m pip install -r requirements.txt
	python3 -m pip install pylint
	rm -rf ./build/

.PHONY: clean
clean:
	rm -rf ./build/

.PHONY: build
build:
	docker build -t canary:dev . 

.PHONY: build
dev: build
	docker run canary-dev

.PHONY: lint
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