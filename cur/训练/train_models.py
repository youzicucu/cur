import sys
import os
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout
import torch
import torch.nn as nn
from scipy.stats import poisson
import joblib

# 添加项目根目录到系统路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.config import MODEL_PARAMS

class PoissonModel:
    def __init__(self, iterations=1000, burn_in=100):
        self.iterations = iterations
        self.burn_in = burn_in
        
    def fit(self, home_goals, away_goals):
        # 实现贝叶斯泊松模型的训练
        self.home_lambda = np.mean(home_goals)
        self.away_lambda = np.mean(away_goals)
        
    def predict_proba(self, max_goals=10):
        # 生成比分概率矩阵
        score_probs = np.zeros((max_goals+1, max_goals+1))
        for i in range(max_goals+1):
            for j in range(max_goals+1):
                score_probs[i,j] = (poisson.pmf(i, self.home_lambda) * 
                                  poisson.pmf(j, self.away_lambda))
        return score_probs

class LSTMModel(nn.Module):
    def __init__(self, input_size, hidden_size=64, num_layers=2, dropout=0.2):
        super(LSTMModel, self).__init__()
        self.lstm = nn.LSTM(input_size, hidden_size, num_layers, 
                           batch_first=True, dropout=dropout)
        self.fc = nn.Linear(hidden_size, 3)  # 3 classes: win, draw, lose
        
    def forward(self, x):
        lstm_out, _ = self.lstm(x)
        return self.fc(lstm_out[:, -1, :])

def prepare_data():
    """
    准备训练数据
    返回: X (特征), y (标签)
    """
    # 这里应该实现数据准备的逻辑
    # 包括从数据库加载数据，特征工程等
    pass

def train_poisson_model(X, y):
    """
    训练泊松模型
    """
    model = PoissonModel(**MODEL_PARAMS['poisson'])
    model.fit(X['home_goals'], X['away_goals'])
    return model

def train_random_forest(X, y):
    """
    训练随机森林模型
    """
    model = RandomForestClassifier(**MODEL_PARAMS['random_forest'])
    model.fit(X, y)
    return model

def train_lstm(X, y):
    """
    训练LSTM模型
    """
    params = MODEL_PARAMS['lstm']
    model = Sequential([
        LSTM(params['units'], return_sequences=True, input_shape=(X.shape[1], X.shape[2])),
        Dropout(params['dropout']),
        LSTM(params['units']),
        Dropout(params['dropout']),
        Dense(3, activation='softmax')
    ])
    
    model.compile(optimizer='adam',
                 loss='categorical_crossentropy',
                 metrics=['accuracy'])
    
    model.fit(X, y, 
              epochs=params['epochs'],
              batch_size=params['batch_size'],
              validation_split=0.2)
    
    return model

def main():
    # 准备数据
    X, y = prepare_data()
    
    # 训练模型
    print("训练泊松模型...")
    poisson_model = train_poisson_model(X, y)
    
    print("训练随机森林模型...")
    rf_model = train_random_forest(X, y)
    
    print("训练LSTM模型...")
    lstm_model = train_lstm(X, y)
    
    # 保存模型
    save_dir = '/content/drive/MyDrive/football_models'
    os.makedirs(save_dir, exist_ok=True)
    
    joblib.dump(poisson_model, f'{save_dir}/poisson_model.joblib')
    joblib.dump(rf_model, f'{save_dir}/random_forest_model.joblib')
    tf.keras.models.save_model(lstm_model, f'{save_dir}/lstm_model')
    
    print("所有模型训练完成并保存")

if __name__ == "__main__":
    main() 