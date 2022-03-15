.PHONY: clean
clean:
	rm -rf ./build

.PHONY: build
build: clean
	mkdir ./build
	cd ./build && cmake ../src/ && cmake --build .

.PHONY: run
run: build
	./build/c_06