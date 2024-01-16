# GPIO

## LED灯控制
![本地·](<../../Document images/MCU/g431_led原理图.png>)

![本地](<../../Document images/MCU/g431_led管脚.png>)
* 在控制引脚电平时需要先给LED数据锁存器使能
```c
void led_work(uint16_t LED_Pin,uint8_t mode)
{
    HAL_GPIO_WritePin(GPIOD, GPIO_PIN_2, GPIO_PIN_SET);
    if(mode) HAL_GPIO_WritePin(GPIOC, LED_Pin, GPIO_PIN_RESET);
    else HAL_GPIO_WritePin(GPIOC, LED_Pin, GPIO_PIN_SET);
}
```