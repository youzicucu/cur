# 足球预测模型训练指南

## 环境准备

1. 访问 [Google Colab](https://colab.research.google.com/)
2. 登录您的Google账户
3. 创建新的笔记本

## 训练步骤

1. 首先在Colab中安装必要的依赖：
```python
!pip install -r requirements.txt
```

2. 挂载Google Drive以保存模型：
```python
from google.colab import drive
drive.mount('/content/drive')
```

3. 克隆项目代码：
```python
!git clone [您的GitHub仓库地址]
```

4. 运行训练脚本：
```python
!python train_models.py
```

## 模型保存

训练完成后，模型会自动保存到Google Drive中的指定目录。您可以下载这些模型文件并上传到您的GitHub仓库。

## 注意事项

1. 确保您的Google Drive有足够的存储空间
2. 建议使用GPU运行时以加快训练速度：
   - 运行时 -> 更改运行时类型 -> GPU

## 定期重训练

为了保持模型的准确性，建议每周重新训练一次模型，更新最新的比赛数据。

## 故障排除

如果遇到内存不足的问题：
1. 减小批次大小
2. 减少训练轮数
3. 使用数据生成器
4. 清理不必要的变量

如果遇到训练时间过长：
1. 使用GPU运行时
2. 减少数据量
3. 简化模型结构 