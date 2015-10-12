'''
Created on 2 Jun 2015

@author: michal
'''
import GPy
import numpy as np

def single_task_kernel(indices_features, ARD, ktype, name):
    active_dims=np.array(indices_features)
    if ktype=="RBF" or ktype=="RBF+Bias":
        if ARD:
            variance=np.ones_like(active_dims)
        else:
            variance=1
        k1=GPy.kern.RBF(len(indices_features),
                             variance=variance,
                             lengthscale=1,
                             active_dims=active_dims, 
                             ARD=ARD, name=name)
    if ktype=="LIN" or ktype=="LIN+Bias":
        if ARD:
            variances=np.ones_like(active_dims)
        else:
            variances=1
        k1=GPy.kern.Linear(len(indices_features),
                             variances=variances,
                             active_dims=active_dims, 
                             ARD=ARD, name=name)
    
    if ktype=="LIN+Bias" or ktype=="RBF+Bias":
        k1=k1+GPy.kern.Bias(len(indices_features))
    return k1
def multi_task_kernel(tasks_number, index_task, k1):
    W = np.ones((tasks_number, 1))*0.3
    # Here we assume, that the column number where the task id is stored is the last column:
    k2 = GPy.kern.Coregionalize(input_dim=1, output_dim=tasks_number, rank=1, active_dims=index_task, W = W)
    pW =  k2['.*W.*']
    pW.constrain_positive()
    k2['.*kappa.*'] = np.ones_like(k2['.*kappa.*'])*0.9
    
    kernel = k1*k2
    return kernel

def multi_task_kernel_pooled_init(tasks_number, index_task, k1):
    W = np.ones((tasks_number, 1))*(1.0/np.sqrt(tasks_number))
    # Here we assume, that the column number where the task id is stored is the last column:
    k2 = GPy.kern.Coregionalize(input_dim=1, output_dim=tasks_number, rank=1, active_dims=index_task, W = W)
    pW =  k2['.*W.*']
    pW.constrain_positive()
    k2['.*kappa.*'] = np.zeros_like(k2['.*kappa.*'])
    
    kernel = k1*k2
    return kernel

def multi_task_kernel_pooled_fixed(tasks_number, index_task, k1):
    W = np.ones((tasks_number, 1))
    # Here we assume, that the column number where the task id is stored is the last column:
    k2 = GPy.kern.Coregionalize(input_dim=1, output_dim=tasks_number, rank=1, active_dims=index_task, W = W)
    k2['.*kappa.*'] = np.zeros_like(k2['.*kappa.*'])
    k2['.*kappa.*'].fix()
    k2['.*W.*'].fix()
    
    kernel = k1*k2
    return kernel
