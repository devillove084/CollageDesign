import numpy as np
import uuid
from functools import namedtuple

import pycuda.autoinit
import pycuda.gpuarray as gpuarray
import pycuda.driver as drv

import skcuda.linalg as culinalg
import skcuda.misc as cumisc
culinalg.init()


def load_data(filename):
    dataset = []
    with open(filename, 'r') as f:
        for line in f:
            line_data = [float(data) for data in line.split()]
            dataset.append(line_data)
    dataset = np.array(dataset)
    return gpuarray.to_gpu(dataset)

def split_dataset(dataset,feat_idx,value):
    ldata,rdata = [], []
    for data in dataset:
        if data[feat_idx] < value:
            ldata.append(data)
        else:
            rdata.append(data)
    
    return ldata,rdata

def fleaf(dataset):
    ''' 计算给定数据的叶节点数值, 这里为均值
    '''
    #dataset = np.array(dataset)
    return cumisc.mean(dataset[:,-1])

def ferr(dataset):
    #dataset = np.array(dataset)
    m, _ = dataset.shape
    return cumisc.var(dataset[:, -1])*dataset.shape[0]

def choose_best_feature(dataset,fleaf,ferr,opt):
    ''' 选取最佳分割特征和特征值

    dataset: 待划分的数据集
    fleaf: 创建叶子节点的函数
    ferr: 计算数据误差的函数
    opt: 回归树参数.
        err_tolerance: 最小误差下降值;
        n_tolerance: 数据切分最小样本数
    '''
    #dataset = np.array(dataset)
    m,n = dataset.shape
    err_tolerance,n_tolerance = opt['err_tolerance'], opt['n_tolerance']

    #遍历所有特征
    err = ferr(dataset)
    best_feat_idx,best_feat_val,best_err = 0,0,float('inf')
    for feat_idx in range(n-1):
        values = dataset[:, feat_idx]
        #遍历所有特征值
        for value in values:
            ldata,rdata = split_dataset(dataset.tolist(),feat_idx,value)
            if len(ldata) < n_tolerance or len(rdata) < n_tolerance:
                #如果切分的样本量太小
                continue
            
            new_err = ferr(ldata) + ferr(rdata)
            if new_err < best_err:
                best_feat_idx = feat_idx
                best_feat_val = value
                best_err = new_err
            
    #如果误差变化不大归为一类
    if abs(err - best_err) < err_tolerance:
        return None, fleaf(dataset)
    
    #检查分类样本是否太小
    ldata, rdata = split_dataset(dataset.tolist(),best_feat_idx,best_feat_val)
    if len(ldata) < n_tolerance or len(rdata) < n_tolerance:
        return None, fleaf(dataset)
    return best_feat_idx, best_feat_val


def create_tree(dataset,fleaf,ferr,opt=None):
    ''' 递归创建树结构

    dataset: 待划分的数据集
    fleaf: 创建叶子节点的函数
    ferr: 计算数据误差的函数
    opt: 回归树参数.
        err_tolerance: 最小误差下降值;
        n_tolerance: 数据切分最小样本数
    '''
    if opt is None:
        opt = {'err_tolerance':1,'n_tolerance':4}
    
    feat_idx,value = choose_best_feature(dataset,fleaf,ferr,opt)
    
    if feat_idx is None:
        return value
    
    tree = {'feat_idx': feat_idx,'feat_val':value}
    
    
    ldata,rdata = split_dataset(dataset,feat_idx,value)
    ltree = create_tree(ldata,fleaf,ferr,opt)
    rtree = create_tree(rdata,fleaf,ferr,opt)
    tree['left'] = ltree
    tree['right'] = rtree

    return tree

def get_nodes_edges(tree, root_node=None):
    '''返回树中所有的节点和边
    '''
    Node = namedtuple('Node',['id','label'])
    Edge = namedtuple('Edge',['start','end'])

    nodes,edges = [],[]
    if type(tree) is not dict:
        print('We need DICTS!!!')
        return nodes,edges

    if root_node is None:
        label = '{}:{}'.format(tree['feat_idx'],tree['feat_val'])
        root_node = Node._make([uuid.uuid4(), label])
        nodes.append(root_node)

    for sub_tree in (tree['left'],tree['right']):
        if type(sub_tree) is dict:
            node_label = '{}: {}'.format(sub_tree['feat_idx'],sub_tree['feat_val'])
        else:
            node_label = '{:.2f}'.format(sub_tree)
        sub_node = Node._make([uuid.uuid4(), node_label])
        nodes.append(sub_node)

        edge = Edge._make([root_node,sub_node])
        edges.append(edge)

        sub_nodes, sub_edges = get_nodes_edges(sub_tree, root_node=sub_node)
        nodes.extend(sub_nodes)
        edges.extend(sub_edges)

    return nodes, edges

def dotify(tree):
    ''' 获取树的Graphviz Dot文件的内容
    '''
    content = 'digraph decision_tree {\n'
    nodes, edges = get_nodes_edges(tree)

    for node in nodes:
        content += '    "{}" [label="{}"];\n'.format(node.id, node.label)

    for edge in edges:
        start, end = edge.start, edge.end
        content += '    "{}" -> "{}";\n'.format(start.id, end.id)
    content += '}'

    return content

def make_dotfile(tree):
    dotfile = 'test.dot'
    with open(dotfile,'w') as f:
        content = dotify(tree)
        f.write(content)

def tree_predict(data, tree):
    ''' 递归根据给定的回归树预测数据值
    '''
    if type(tree) is not dict:
        return tree

    feat_idx, feat_val = tree['feat_idx'], tree['feat_val']
    if data[feat_idx] < feat_val:
        sub_tree = tree['left']
    else:
        sub_tree = tree['right']

    return tree_predict(data, sub_tree)

def not_tree(tree):
    return type(tree) is not dict

def collapse(tree):
    ''' 对一棵树进行塌陷处理, 得到给定树结构的平均值
    '''
    if not_tree(tree):
        return tree
    ltree,rtree = tree['left'] ,tree['right']
    return (collapse(ltree) + collapse(rtree))/2

def postprune(tree, test_data):
    ''' 根据测试数据对树结构进行后剪枝
    '''
    if not_tree(tree):
        return tree
    
    if not test_data:
        return collapse(tree)

    ltree,rtree = tree['left'], tree['right']

    if not_tree(ltree) and not_tree(rtree):
        ldata,rdata = split_dataset(test_data,tree['feat_idx'],tree['feat_val'])

        err_no_merge = (np.sum((np.array(ldata) - ltree)**2) + 
                        np.sum((np.array(rdata) - rtree)**2))
        
        err_merge = np.sum((np.array(test_data) - (ltree + rtree)/2)**2)

        if err_merge < err_no_merge:
            print('Merge!')
            return (ltree + rtree)/2
        else:
            return tree
        
        tree['left'] = postprune(tree['left'],test_data)
        tree['right'] = postprune(tree['right'],test_data)

        return tree

def get_corrcoef(X,Y):
    cov = np.mean(X*Y) - np.mean(X)*np.mean(Y)
    return cov/(np.var(X)*np.var(Y))**0.5



    