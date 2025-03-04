# 模型文件目录

此目录用于存放训练好的模型文件。从Google Colab训练完成后，请将以下文件下载并放置在此目录中：

1. `poisson_model.joblib` - 泊松分布模型
2. `random_forest_model.joblib` - 随机森林模型
3. `lstm_model/` - LSTM神经网络模型（目录）

## 模型更新流程

1. 在Google Colab中完成模型训练
2. 从Google Drive的`/content/drive/MyDrive/football_models/`目录下载最新的模型文件
3. 将下载的模型文件放置在此目录中
4. 提交到GitHub仓库

## 注意事项

- 定期更新模型以保持预测准确性
- 保留模型的版本历史记录
- 在更新模型前，建议备份当前使用的模型文件 