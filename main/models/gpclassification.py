'''
Created on 7 Feb 2015

@author: michal
'''
import pickle
import GPy
import numpy as np

class GPClassifier(object):
    '''
    classdocs
    '''
    def __init__(self, kernel_constructor, name=None, RANDOM_RESTARTS=-1, optimize=True, matrixify_y=True):
        '''
        Constructor
        '''
        self.kernel_constructor = kernel_constructor
        self.name = name
        self.RANDOM_RESTARTS = RANDOM_RESTARTS
        self.optimize = optimize
        self.matrixify_y = matrixify_y
        
    def fit(self, X, y, optimize=True):
        print "[GPClassifier.fit] Setting up model..."
        
        if self.matrixify_y:
            y = np.matrix(y[:, None])
        
        self.m = GPy.models.GPClassification(X, y, kernel=self.kernel_constructor())
        if self.optimize:
            print "[GPClassifier.fit] Optimizing..."
            if self.RANDOM_RESTARTS > 1:
                self.m.optimize_restarts(messages=False, robust=True, num_restarts=self.RANDOM_RESTARTS)
            else:
                self.m.optimize(messages=True)
        
    def predict(self, X):
        mean, var = self.m.predict(X)
        #print "[GPClassifier.predict_vector] mean:", mean
        predicted = np.round(mean)
        return predicted
    
    def get_params(self, deep=False):
        return self.__dict__