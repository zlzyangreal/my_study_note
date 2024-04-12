因为lcd屏幕使用时动了灯的管脚，还原灯管脚就行
## 方法
在 `LCD_WriteReg` `LCD_WriteRAM_Prepare` `LCD_WriteRAM`函数首尾分别加上
```c
unsigned short PCOUT = GPIOC->ODR;

GPIOC->ODR = PCOUT;
```