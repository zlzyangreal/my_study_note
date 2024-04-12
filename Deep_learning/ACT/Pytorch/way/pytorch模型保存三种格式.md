
## 保存整个模型
```python
#模型保存
torch.save(model,"PATH")
#模型加载
model = torch.load("PATH")
#设置模型进行测试模型
model.eval()
```

## 仅保存模型的各项参数
```python
#其中model.state dict()表示模型的各项参数
torch.save(model.state_dict(),"PATH")
#加载模型，注意！！这种方式首先需要将模型的原型写出后，才能加载模型的各项指标参数
model = TheModelClass(*arg,*kwargs)
model.load_state_dict(torch.load("PATH"))
```

## TorchScript形式(该形式才能用于推理)
```python
model_scripted = torch.jit.script(model)
model_scripted.save("model_scripted.pt")
model = torch.jit.load("model_scripted.pt")
model.eval()
```