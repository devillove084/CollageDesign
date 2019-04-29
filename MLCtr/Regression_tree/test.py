from regression_tree_cu import *
import numpy as np
import matplotlib.pyplot as plt

# if '__main__' == __name__:
#     datafile = 'ex0.txt'
#     dataset = load_data(datafile)
#     tree = create_tree(dataset, fleaf, ferr, opt={'n_tolerance':4,'err_tolerance':1})

#     dotfile = '{}.dot'.format(datafile.split('.')[0])
#     with open(dotfile,'w') as f:
#         content = dotify(tree)
#         f.write(content)

#     dataset = np.array(dataset)
#     plt.scatter(dataset[:,0],dataset[:,1])
#     x = np.linspace(0,1,50)
#     y = [tree_predict([i],tree) for i in x]
#     plt.plot(x,y,c='r')
#     plt.show()

if '__main__' == __name__:
    data_train = load_data('train.txt')
    data_test = load_data('test.txt')

    dataset_test = np.matrix(data_test)
    m,n = dataset_test.shape
    testset = np.ones((m,n+1))
    testset[:, 1:] = dataset_test
    X_test, y_test = testset[:,:-1],testset[:,-1]

    tree = create_tree(data_train,fleaf,ferr,opt={'err_tolerance': 1,'n_tolerance': 4})
    make_dotfile(tree)
    y_tree = [tree_predict([x],tree) for x in X_test[:,1].tolist()]
    y_tree = postprune(y_tree,data_test)
    
    corrcoef_tree = get_corrcoef(np.array(y_tree), y_test)

    plt.scatter(np.array(data_train)[:, 0], np.array(data_train)[:,1])
    x = np.sort([i for i in X_test[:, 1].tolist()])
    y = [tree_predict([i], tree) for i in x]
    plt.plot(x, y, c='y')
    plt.show()
