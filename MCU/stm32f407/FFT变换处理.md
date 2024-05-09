具体函数在 `E:\Data\MCU_Project\Stm32_Project\BSP_MATH\FFT\mdeal\fftdeal.c`
## 1.去直流
"去直流"是指从信号中移除直流分量，也就是信号中的零频率成分。直流分量代表信号的偏移量，它的频率为零

函数实现
```c
void removeDC(void) {
  float32_t mean = 0.0;
    int i;
    for(i=0;i<fft_size;i++) {
      mean += (float)(ADC_Buffer[i]*3.3/4096);
    }
    mean /=fft_size;
    for(i=0;i<fft_size;i++) {
      input_signal[i] = (float)(ADC_Buffer[i]*3.3/4096) - mean;
    }
}
```
* 在时域上将偏移量完全减掉
## 2.加窗(会优化，但是不一定有必要)
## 3.FFT数据存入
```c
    for(i=0;i<FFT_SIZE;i++) {
      FFT_Input[2*i] = (float)(signal[i]);
      FFT_Input[2*i+1] = 0;
    }
```
* 实部存入，虚部为0
* 在使用FFT进行变换时，输入信号通常是一个实数序列。FFT算法要求输入序列具有对称性，即实部是奇对称的，虚部是偶对称的。由于实部是奇对称的，它的频谱是纯虚数，而虚部是偶对称的，它的频谱是纯实数。为了满足这种对称性要求，可以将实数序列作为FFT的输入，并将其虚部设置为零。这样做的原因是，FFT算法是基于复数运算的，它将实数序列视为虚部为零的复数序列进行处理。因此，将实部存入，而将虚部设置为零可以满足FFT算法的输入要求，并且可以正确地计算出频域表示。当进行FFT变换后，得到的频域表示是一个复数序列，其中实部表示信号的幅度，虚部表示信号的相位。通过对频域表示进行逆FFT变换，可以还原原始的实数序列。
## 4.使用 ARM CMSIS DSP 库中的函数来执行基于 ARM Cortex-M 处理器的快速傅里叶变换（FFT）操作
```c
arm_cfft_f32(&arm_cfft_sR_f32_len1024,FFT_Input,ifftFlag,doBitReverse);
```
* 示例结构体arm_cfft_sR_f32_len1024(1024个数)
* FFT_Input FFT数组
* `ifftFlag` 和 `doBitReverse` 是用于控制 FFT 变换的标志位(这里我`ifftFlag是0``doBitReverse是1`)
## 5.得到频域值
```c
arm_cmplx_mag_f32(FFT_Input, FFT_Output, fft_size);
```
## 6.计算电压幅值、频率大小
设ADC采样频率为f,采样点数为N,FFT_Output 对应最大值索引是k
```bash
电压幅值
FFT_Output/(N/2)
波形频率
f0=(k*f)/N
```
