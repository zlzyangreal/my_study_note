# 静态数据

和C++stacte一样，这个只能模块内使用
```verilog
module MyModule;
  // 声明 localparam
  localparam WIDTH = 8;
  localparam HEIGHT = 16;
  
  // 模块的其他部分
  // ...
  
endmodule
```