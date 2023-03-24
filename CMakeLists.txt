cmake_minimum_required(VERSION 3.24)
project(merge-sort)

set(CMAKE_CXX_STANDARD 23)

find_package(OpenMP REQUIRED)
add_executable(merge-sort main.cpp)
target_link_libraries(merge-sort PRIVATE OpenMP::OpenMP_CXX)

