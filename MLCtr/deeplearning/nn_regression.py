import numpy as np
import torch as T  # non-standard alias

def accuracy(model, data_x, data_y, pct_close):
  n_items = len(data_y)
  X = T.Tensor(data_x).cuda()  # 2-d Tensor
  Y = T.Tensor(data_y).cuda()  # actual as 1-d Tensor
  oupt = model(X)       # all predicted as 2-d Tensor
  pred = oupt.view(n_items)  # all predicted as 1-d
  n_correct = T.sum((T.abs(pred - Y) < T.abs(pct_close * Y)))
  result = (n_correct.item() * 100.0 / n_items)  # scalar
  return result 

class Net(T.nn.Module):
  def __init__(self):
    super(Net, self).__init__()
    self.hid1 = T.nn.Linear(13, 10)  # 13-(10-10)-1
    self.hid2 = T.nn.Linear(10, 10)
    self.oupt = T.nn.Linear(10, 1)
    T.nn.init.xavier_uniform_(self.hid1.weight)  # glorot
    T.nn.init.zeros_(self.hid1.bias)
    T.nn.init.xavier_uniform_(self.hid2.weight)
    T.nn.init.zeros_(self.hid2.bias)
    T.nn.init.xavier_uniform_(self.oupt.weight)
    T.nn.init.zeros_(self.oupt.bias)
  def forward(self, x):
    z = T.tanh(self.hid1(x))
    z = T.tanh(self.hid2(z))
    z = self.oupt(z)  # no activation, aka Identity()
    return z

def main():
  # 0. Get started
  print("\nBoston regression using PyTorch 1.0 \n")
  T.cuda.manual_seed(1);  np.random.seed(1)
  # 1. Load data
  print("Loading Boston data into memory ")
  train_file = "boston_train.txt"
  test_file = "boston_test.txt"
  train_x = np.loadtxt(train_file, delimiter="\t",
    usecols=range(0,13), dtype=np.float32)
  train_y = np.loadtxt(train_file, delimiter="\t",
    usecols=[13], dtype=np.float32)
  test_x = np.loadtxt(test_file, delimiter="\t",
    usecols=range(0,13), dtype=np.float32)
  test_y = np.loadtxt(test_file, delimiter="\t",
    usecols=[13], dtype=np.float32)

  # 2. Create model
  print("Creating 13-(10-10)-1 DNN regression model \n")
  net = Net().cuda()  # all work done above

  # 3. Train model
  net = net.train()  # set training mode

  bat_size = 10

  loss_func = T.nn.MSELoss()  # mean squared error
  optimizer = T.optim.SGD(net.parameters(), lr=0.01)

  n_items = len(train_x)
  print(n_items)
  batches_per_epoch = n_items // bat_size
  max_batches = 1000 * batches_per_epoch
  print("Starting training")
  
  for b in range(max_batches):
    curr_bat = np.random.choice(n_items, bat_size,replace=False)
    X = T.Tensor(train_x[curr_bat]).cuda()
    Y = T.Tensor(train_y[curr_bat]).view(bat_size,1).cuda()
    
    optimizer.zero_grad()
    oupt = net(X)
    loss_obj = loss_func(oupt, Y)
    loss_obj.backward()
    optimizer.step()
    
    if b % (max_batches // 10) == 0:
      print("batch = %6d" % b, end="")
      print("  batch loss = %7.4f" % loss_obj.item(), end="")
      net = net.eval()
      acc = accuracy(net, train_x, train_y, 0.15)
      net = net.train()
      print("  accuracy = %0.2f%%" % acc)      
  print("Training complete \n")
  
  # 4. Evaluate model
  net = net.eval()  # set eval mode
  acc = accuracy(net, test_x, test_y, 0.15)
  print("Accuracy on test data = %0.2f%%" % acc)
  # 5. Save model - TODO
  # 6. Use model
  raw_inpt = np.array([[0.09266, 34, 6.09, 0, 0.433, 6.495, 18.4,
    5.4917, 7, 329, 16.1, 383.61, 8.67]], dtype=np.float32)
  norm_inpt = np.array([[0.000970, 0.340000, 0.198148, -1,
    0.098765, 0.562177, 0.159629, 0.396666, 0.260870, 0.270992,
    0.372340, 0.966488, 0.191501]], dtype=np.float32)
  X = T.Tensor(norm_inpt).cuda()
  y = net(X)
  print("For a town with raw input values: ")
  for (idx,val) in enumerate(raw_inpt[0]):
    if idx % 5 == 0: print("")
    print("%11.6f " % val, end="")
  print("\n\nPredicted median house price = $%0.2f" %
    (y.item()*10000))
if __name__=="__main__":
  main()