# VS使用基础配置

注意:VS内部文件放置位置和外部文件位置无关

新项目创建
----------
1. 创建解决方案以及项目名称
2. 创建总文件夹资源文件
`$(ProjectDir)bin\$(Platform)\$(Configuration)\`
3. 创建项目输出文件以及中间文件并且配置
`$(ProjectDir)tmp\$(Platform)\$(Configuration)\`
4. 拉入程序以及头文件等
5. 配置各文件路径
6. 注意平台配置