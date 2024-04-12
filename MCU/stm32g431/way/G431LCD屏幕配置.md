## LCD管脚原理图
![[g431_lcd管脚.png]]
## 初始化
```c
  LCD_Init();
  LCD_SetTextColor(Black);
  LCD_SetBackColor(Yellow);
```
## 显示
```c
    sprintf((char*)lcd_disp_str,"aaa");
    LCD_DisplayStringLine(Line0,lcd_disp_str);
    HAL_GPIO_WritePin(GPIOD, GPIO_PIN_2, GPIO_PIN_SET);
    HAL_GPIO_WritePin(GPIOC, GPIO_PIN_All, GPIO_PIN_SET);
    HAL_GPIO_WritePin(GPIOD, GPIO_PIN_2, GPIO_PIN_RESET);
```
* 横排20字
* 与灯会冲突加上关了灯