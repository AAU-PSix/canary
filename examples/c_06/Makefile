.PHONY: clean
clean:
	rm -rf ./build

.PHONY: build
build: clean
	mkdir -p ./build
	cd ./build && cmake ../ && cmake --build .

.PHONY: run
run: build
	./build/c_06

.PHONY: test
test: build
	./build/c_06_test

up:
	docker-compose up