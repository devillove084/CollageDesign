import torch
import torch.nn as nn
from torch.autograd import Variable
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

#from graduateutil import train_test_split

# 超参数
TIME_STEP = 10  # rnn time step  
INPUT_SIZE = 1  # rnn input size
LR = 0.02  # learn rate
 
 
# show data
#steps = np.linspace(0, np.pi*2, 100, dtype=np.float32)
#x_np = np.sin(steps)  # float32 for converting torch FloatTensor
#y_np = np.cos(steps)
data = pd.read_csv('../data/TempLinkoping2016.txt', sep="\t")

x = np.atleast_3d(data["time"].values)
y = np.atleast_3d(data["temp"].values)

#x = time.reshape((-1, 1))               # Time. Fraction of the year [0, 1]
#x = np.insert(x, 0, values=1, axis=1)   # Insert bias term
#y = temp[:, 0]                          # Temperature. Reduce to one-dim
#X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.5)
 
 
class RNN(nn.Module):
    def __init__(self):
        super(RNN, self).__init__()
        self.rnn = nn.RNN(
            input_size=INPUT_SIZE,
            hidden_size=32,  # rnn hidden unit
            num_layers=1,  # number of rnn layer
            # input & output will has batch size as 1s dimension
            # (batch, time_step, input_size)
            batch_first=True,
        )
        self.out = nn.Linear(32, 1)
        
    def forward(self, x, h_state):
        # x (batch, time_step, input_size)
        # h_state (n_layers, batch, hidden_size)
        # r_out (batch, time_step, hidden_size)
        r_out, h_state = self.rnn(x, h_state)
        
        outs = []  # save all predictions
        for time_step in range(r_out.size(1)):  # calculate output for each time step  
            outs.append(self.out(r_out[:, time_step, :]))
        return torch.stack(outs, dim=1), h_state
 
 
rnn = RNN().cuda()
#print(rnn)
 
 
optimizer = torch.optim.SGD(rnn.parameters(), lr=0.05)
loss_func = torch.nn.MSELoss()
h_state = None  # for initial hidden state
 
 
plt.figure(1, figsize=(12, 5))
plt.ion()

for step in range(600):
    #start, end = step * np.pi, (step+1)*np.pi  # time range
    # use sin predicts cos
    #steps = np.linspace(start, end, TIME_STEP, dtype=np.float32)
    #x_np = np.sin(steps)
    #y_np = np.cos(steps)
    #x = Variable(torch.from_numpy(x_np[np.newaxis, :, np.newaxis])).cuda()
    #y = Variable(torch.from_numpy(y_np[np.newaxis, :, np.newaxis])).cuda()
    
    x = Variable(torch.from_numpy(x)).cuda()
    y = Variable(torch.from_numpy(y)).cuda()

    prediction, h_state = rnn(x, h_state)
    h_state = Variable(h_state.data).cuda()
    
    loss = loss_func(prediction, y)
    optimizer.zero_grad()
    loss.backward()
    optimizer.step()
    
    # plotting
    plt.plot(steps, y_np.flatten(), 'r-')
    plt.plot(steps, prediction.data.cpu().numpy().flatten(), 'b-')
    plt.pause(0.05)
plt.ioff()
plt.show()