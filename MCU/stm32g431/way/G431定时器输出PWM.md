cubemax配置
## 1.选择引脚
![[g431pwm1.png]]
* 这里尽量选择通道一免得引脚复用
## 2.开启PWM模式
![[g431pwm2.png]]
## 3.配置频率以及占空比
![[g431pwm3.png]]
![[g431pwm4.png]]
* 这里以频率1K，占空比0.5为例
## 4.初始化打开PWM
```c
HAL_TIM_PWM_Start(&htim16,TIM_CHANNEL_1);
```
## 5.设置比较值
```c
__HAL_TIM_SetCompare(&htim16,TIM_CHANNEL_1,400);
```