#!/bin/bash
set -e
if [ ! -d "build" ]; then
  echo "build文件夹不存在，正在创建..."
  mkdir build
  echo "build文件夹创建成功！"
else
  echo "build文件夹已存在。"
fi

cd build

cmake ..

make

./open