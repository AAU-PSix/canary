cmake_minimum_required(VERSION 3.0.2)

# set the project name
project(c_06)

add_executable(c_06_test AllTests.c CuTest.c)
add_test(NAME c_06_test COMMAND c_06_test)

# add the executable
add_executable(c_06 original.c)