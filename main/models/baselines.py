'''
Created on 16 May 2015

@author: michal
'''
from sklearn.metrics import accuracy_score 
from sklearn.grid_search import GridSearchCV
from sklearn.svm.classes import SVC
from sklearn.dummy import DummyClassifier
from sklearn import linear_model
tuned_parametersRBF_SVM = [{'kernel': ['rbf'], 'gamma': [1e-3, 1e-4],
                     'C': [0.00001, 0.0001, 0.001, 0.1, 1, 10, 100]}]
tuned_parametersLIN_SVM = [{'kernel': ['linear'], 
                     'C': [0.00001, 0.0001, 0.001, 0.1, 1, 10, 100]}]

tuned_parametersLR = [{'C': [0.00001, 0.0001, 0.001, 0.1, 1, 10, 100]}]



class SklearnBaseline(object):
    def __init__(self, cls, name, features):
        #print "[SklearnBaseline.__init__] cls", cls, "name", name
        self.name=name
        self.features=features
        self.m=cls()
    def predict(self, x):
        return self.m.predict(x[:, self.features])
    def fit(self, X, y):
        return self.m.fit(X[:, self.features], y)

class SVM(object):
    '''
    classdocs
    '''
    def __init__(self, kernel, name, features):
        '''
        Constructor
        '''
        self.name = name
        self.features=features
        
        if kernel=="LIN":
            self.tuned_parameters=tuned_parametersLIN_SVM
        if kernel=="RBF":
            self.tuned_parameters=tuned_parametersRBF_SVM
        self.clf = GridSearchCV(SVC(C=1), self.tuned_parameters, n_jobs=4,
                       score_func=accuracy_score)
    
    def fit(self, X, y):
        Xin=X[:, self.features]
        try:
            self.clf.fit(Xin, y)
            print "[SVM] learned hyperparameters:", self.clf.best_estimator_
        except:
            print "[SVM] Exception in fit, using Most Frequent class instead!"
            #self.clf=SklearnBaseline(lambda: SVC(C=1, kernel=self.tuned_parameters[0]['kernel'][0]), "")
            self.clf=SklearnBaseline(lambda: DummyClassifier("most_frequent"), "", [])
            self.clf.fit(Xin, y)
    
    def predict(self, X):
        return self.clf.predict(X[:, self.features])
    
class LR(object):
    '''
    classdocs
    '''
    def __init__(self, name, features):
        '''
        Constructor
        '''
        self.name = name
        self.features=features
        
        self.tuned_parameters=tuned_parametersLR
        self.clf = GridSearchCV(linear_model.LogisticRegression(C=1, penalty='l1'), self.tuned_parameters, n_jobs=4,
                       score_func=accuracy_score)
    
    def fit(self, X, y):
        Xin=X[:, self.features]
        try:
            self.clf.fit(Xin, y)
            print "[LR] learned hyperparameters:", self.clf.best_estimator_
        except:
            print "[LR] Exception in fit, using Most Frequent class instead!"
            #self.clf=SklearnBaseline(lambda: SVC(C=1, kernel=self.tuned_parameters[0]['kernel'][0]), "")
            self.clf=SklearnBaseline(lambda: DummyClassifier("most_frequent"), "", [])
            self.clf.fit(Xin, y)
    
    def predict(self, X):
        return self.clf.predict(X[:, self.features])
    