
cmake_minimum_required(VERSION 3.5)
project(assem1_urdf)

find_package(ament_cmake REQUIRED)

install(DIRECTORY urdf meshes launch config
  DESTINATION share/${PROJECT_NAME}
)

ament_package()
