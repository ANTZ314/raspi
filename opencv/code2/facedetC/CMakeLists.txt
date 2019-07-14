
cmake_minimum_required(VERSION 2.8)
project( FaceDet )
find_package( OpenCV REQUIRED )
include_directories( ${OpenCV_INCLUDE_DIRS} )
add_executable( FaceDet FaceDet.cpp )
target_link_libraries( FaceDet ${OpenCV_LIBS} )
