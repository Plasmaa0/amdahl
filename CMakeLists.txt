cmake_minimum_required(VERSION 3.24)
project(osi2)

set(CMAKE_CXX_STANDARD 23)

find_package(OpenMP REQUIRED)
add_executable(osi2 main.cpp)
target_link_libraries(osi2 PRIVATE OpenMP::OpenMP_CXX)

