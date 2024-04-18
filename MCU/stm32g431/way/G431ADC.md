## ADC原理图
![[g431adc.png]]
## cubemax
#### 1.选择引脚
![[g431adc1.png]]
#### 2.开启对于adc通道
![[g431adc2.png]]
* 其他参数不用设置因为只是简单运用
## 编程
```c
double getADC(ADC_HandleTypeDef *pin) {
    uint32_t adc;
    HAL_ADC_Start(pin);
    adc = HAL_ADC_GetValue(pin);
    return adc*3.3/4096;
}
```