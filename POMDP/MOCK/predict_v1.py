import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np
# 加载模型
loaded_model = ValueNetwork()
loaded_model.load_state_dict(torch.load('value_network.pth'))
loaded_model.eval()

print("Model loaded and ready to use.")
# 使用模型进行预测
test_state = np.random.rand(2)
test_state_tensor = torch.FloatTensor(test_state).unsqueeze(0)
predicted_value = loaded_model(test_state_tensor)
print(f"Predicted value for state {test_state}: {predicted_value.item()}")
