# GPIO

## LED灯控制
![本地·](g431_led原理图.png images/MCU/g431_led原理图.png>)

![本地](g431_led管脚.png images/MCU/g431_led管脚.png>)
* 在控制引脚电平时需要先给LED数据锁存器使能
```c
void led_work(uint16_t LED_Pin,uint8_t mode)
{
    HAL_GPIO_WritePin(GPIOD, GPIO_PIN_2, GPIO_PIN_SET);
    if(mode) HAL_GPIO_WritePin(GPIOC, LED_Pin, GPIO_PIN_RESET);
    else HAL_GPIO_WritePin(GPIOC, LED_Pin, GPIO_PIN_SET);
    HAL_GPIO_WritePin(GPIOD, GPIO_PIN_2, GPIO_PIN_RESET);
}
```
* 使用前全关
## 按键控制
![本地](g431_按键原理图.png images/MCU/g431_按键原理图.png>)

![本地](g431_按键原理图2.png images/MCU/g431_按键原理图2.png>)

![本地](g431_按键管脚.png images/MCU/g431_按键管脚.png>)
```c
////////////////////////////////////////////////////////////////
#define KEY1 HAL_GPIO_ReadPin(GPIOB, GPIO_PIN_0) == GPIO_PIN_RESET
#define KEY2 HAL_GPIO_ReadPin(GPIOB, GPIO_PIN_1) == GPIO_PIN_RESET
#define KEY3 HAL_GPIO_ReadPin(GPIOB, GPIO_PIN_2) == GPIO_PIN_RESET
#define KEY4 HAL_GPIO_ReadPin(GPIOA, GPIO_PIN_0) == GPIO_PIN_RESET
#define ALL_DOWN HAL_GPIO_ReadPin(GPIOB, GPIO_PIN_0) == GPIO_PIN_SET && HAL_GPIO_ReadPin(GPIOB, GPIO_PIN_1) == GPIO_PIN_SET && HAL_GPIO_ReadPin(GPIOB, GPIO_PIN_2) == GPIO_PIN_SET && HAL_GPIO_ReadPin(GPIOA, GPIO_PIN_0) == GPIO_PIN_SET
////////////////////////////////////////////////////////////////
uint8_t key_work(uint8_t mode) {
    static uint8_t key_up = 1;
    key_state = 0;
    if(mode) key_up = 1;
    if(key_up && (KEY1||KEY2||KEY3||KEY4)) {
        HAL_Delay(10);
        key_up = 0;
        if(KEY1) {
            key_state = 1;
            return key_state;
        } else if(KEY2) {
            key_state = 2;
            return key_state;
        } else if(KEY3) {
            key_state = 3;
            return key_state;
        } else if(KEY4) {
            key_state = 4;
            return key_state;
        }
    }else if(ALL_DOWN) {
        key_up = 1;
    }
    return 0;
}
/////////////////////////////////////////////////////////////////////////
```
* [高级按键写法](G431定时器中断)