import torch
import torch.utils.data as utils_data
from torch.autograd import Variable
import numpy as np
from torch import nn, optim
import matplotlib.pyplot as plt

#This is the function the neural network should learn:

def my_funct(x_input):
	y = 0.5*x_input**2 + np.cos(x_input) -  10*np.sin(5*x_input) - 0.1*x_input**3 +x_input + 100
	return y	
# Here I create the training data:	
	
x_train = np.random.uniform(low=-10, high=10, size=23500)
y_train =  my_funct(x_train)

x_train = x_train.reshape(-1,1)
y_train = y_train.reshape(-1,1)

batchsize = 32


training_samples = utils_data.TensorDataset(torch.from_numpy(x_train), torch.from_numpy(y_train))
data_loader = utils_data.DataLoader(training_samples, batch_size=batchsize, shuffle=False)	



# Create the model in Pytorch:

D_in, H_1,H_2,H_3,H_4, H_5,H_6,  D_out = 1, 80,70,60, 40,40,20, 1

model = torch.nn.Sequential(
torch.nn.Linear(D_in, H_1),
torch.nn.ReLU(),
torch.nn.Linear(H_1, H_2),
torch.nn.ReLU(),
#torch.nn.BatchNorm1d(H_2),
torch.nn.Linear(H_2, H_3),
torch.nn.ReLU(),
#torch.nn.BatchNorm1d(H_3),
torch.nn.Linear(H_3, H_4),
torch.nn.ReLU(),
#torch.nn.BatchNorm1d(H_4),
torch.nn.Linear(H_4, H_5),
torch.nn.ReLU(),
torch.nn.Linear(H_5, H_6),
torch.nn.ReLU(),
torch.nn.Linear(H_6, D_out),
)



criterion = nn.MSELoss()
#optimizer = optim.SGD(model.parameters(), lr=1e-4, momentum=0.8)
optimizer = optim.Adam(model.parameters())#, lr=1e-3, momentum=0.8)
model.cuda().train()

num_epochs = 100
loss_list = []

for epoch in range(num_epochs):
	for batch_idx, (data, target) in enumerate(data_loader):
	#print(batch_idx)
		data, target = Variable(data).cuda(), Variable(target).cuda()
		optimizer.zero_grad()
		output = model(data.float())
		loss = criterion(output, target.float())
		#print(batch_idx, loss.data[0])
		loss.backward()
		optimizer.step()
		if epoch >2:
			if batch_idx % 200 == 0:
				loss_list.append(loss.data)
		if batch_idx % 400 == 0:
			print('Train Epoch: {} [{}/{} ({:.0f}%)]\tLoss: {:.6f}'.format(
			epoch, batch_idx * len(data), len(data_loader.dataset),
			100. * batch_idx / len(data_loader), loss.data))

x_train = torch.from_numpy(x_train).float()

y_train = torch.from_numpy(y_train).float()


# plot  the predictions and the difference

model.eval()


prediction = model(Variable(torch.Tensor(np.linspace(-10,10, 10000).reshape(-1,1))).cuda())
prediction = prediction.data.cpu().numpy()

plt.plot(np.linspace(-10,10, 10000), prediction, c= 'r', label='prediction Line')
plt.plot(np.linspace(-10,10, 10000), my_funct( np.linspace(-10,10, 10000)  ), c='c', label='Original data')
plt.legend()

plt.show()


plt.plot(np.linspace(-10,10, 10000), my_funct( np.linspace(-10,10, 10000))- prediction.ravel(), label='difference' )
plt.legend()
plt.show()

plt.plot(loss_list, label='loss')
plt.legend()
plt.show()