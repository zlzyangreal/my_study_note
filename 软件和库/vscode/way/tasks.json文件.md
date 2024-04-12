 tasks.json是 VS Code 中的一个配置文件，用于定义项目中的任务（tasks）
 [copy路径](tasks.json)
 
 ## 例子
 ```json
 {
        "version": "2.0.0",
        "tasks": [
            {
                "label": "build-linux",
                "type": "shell",
                "command": "sudo ./build-linux.sh -t rk3588 -a aarch64 -d wj -b Debug",
                "args": [

                    // linux为空
                ],
                "options": {
                    // 进入build
                    // "${workspaceFolder}/build"：根下
                    // "${fileDirname}"：当前
                    "cwd": "${workspaceFolder}"
                },
                "group": {
                    "kind":"build", // test 任务 和 build 任务不同！
                    "isDefault":true
                }
            },
            {
                "label": "exe",
                "type": "shell",
                "command": "./wj model/yolov8.rknn model/bus.jpg", // 查看本机MinGW, linux下识别核心数
                "args": [
                ],
                "options": {
                    // 进入build
                    // "${workspaceFolder}/bin"：根下
                    // "${fileDirname}"：当前文件的所在文件夹路径
                    "cwd": "${workspaceFolder}/install/rk3588_linux_aarch64/rknn_wj_demo/",
                    "env": {
                        "LD_LIBRARY_PATH": "/home/orangepi/Desktop/WJ/proj/install/rk3588_linux_aarch64/rknn_wj_demo/lib",
                    }
                },
                "group": {
                    "kind":"build",
                    "isDefault":true
                }
            },
            {
                "label":"Build my project", // launch文件需要对应
                "dependsOn":[
                    "build-linux",
                    // "exe",                
                ]
            }
        ]
    }
```