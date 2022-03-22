cmake_minimum_required(VERSION 3.0.2)

# set the project name
project(c_06)

# Build test project
add_executable(c_06_test ./tests/AllTests.c ./tests/CuTest.c)

# add the executable
add_executable(c_06 ./src/original.c)