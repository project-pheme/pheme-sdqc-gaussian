'''
Created on 8 Apr 2015

@author: michal

List of methods for experiments, specified in lists in appropriate functions.
'''
from sklearn.svm.classes import SVC
import GPy
import numpy as np
from main.models.multiclassgp import MCGP
from sklearn.dummy import DummyClassifier
from main.models.baselines import SVM, SklearnBaseline, LR
from main.utils.constants import LABELS
from main.models.gpclassification import GPClassifier
from main.models.feature_indices import get_feature_indices_main_oldexperiments,\
    get_feature_indices_main
from main.models.kernels import single_task_kernel, multi_task_kernel
from sklearn import linear_model
from sklearn.grid_search import GridSearchCV


def get_methods_multitask(tasks_number, header, experimenttype, multiclass, RANDOM_RESTARTS=-1):
    if experimenttype=="old":
        #singletask_summed, _, ALLTEXTFEATURES, index_task=get_feature_indices_main_oldexperiments(header)
        print "[get_methods_multitask] OLD EXPERIMENT IS NOT IMPLEMENTED!!!"
    else:
        singletask_summed_BOW, singletask_summed_BROWN, singletask_summed_BOW_BROWN, ALLFEATURES, ALLTEXTFEATURES, FEATURES_BOW, FEATURES_BROWN, index_task=get_feature_indices_main(header)
    
    if multiclass:
        GPCONSTRUCTOR=lambda kernel_constructor, name, RANDOM_RESTARTS: MCGP(kernel_constructor=kernel_constructor, 
                                                                             labels=LABELS, name=name, RANDOM_RESTARTS=RANDOM_RESTARTS)
    else:
        GPCONSTRUCTOR=GPClassifier
    
    BOW_STR=lambda x: reduce(lambda x, y: x+y, [[header[i] for _ in range(int(x[i]))] for i in FEATURES_BOW])
    BROWN_STR=lambda x: reduce(lambda x, y: x+y, [[header[i] for _ in range(int(x[i]))] for i in FEATURES_BROWN])
    
    METHODS=[
             
             #lambda: GPCONSTRUCTOR(kernel_constructor=lambda: single_task_kernel(FEATURES_BOW, False, "LIN+Bias", "FEATURES_BOW"), name="BOWGPjoinedfeaturesPooledLIN+Bias", 
             #             RANDOM_RESTARTS=RANDOM_RESTARTS),
             #lambda: GPCONSTRUCTOR(kernel_constructor=lambda: single_task_kernel(FEATURES_BROWN, False, "LIN+Bias", "FEATURES_BROWN"), name="BROWNGPjoinedfeaturesPooledLIN+Bias", 
             #             RANDOM_RESTARTS=RANDOM_RESTARTS),
             lambda: GPCONSTRUCTOR(kernel_constructor=lambda: single_task_kernel(FEATURES_BOW, False, "LIN", "FEATURES_BOW"), name="BOWGPjoinedfeaturesPooledLIN", 
                          RANDOM_RESTARTS=RANDOM_RESTARTS),
             lambda: GPCONSTRUCTOR(kernel_constructor=lambda: single_task_kernel(FEATURES_BROWN, False, "LIN", "FEATURES_BROWN"), name="BROWNGPjoinedfeaturesPooledLIN", 
                          RANDOM_RESTARTS=RANDOM_RESTARTS),
             lambda: GPCONSTRUCTOR(kernel_constructor=lambda: single_task_kernel(FEATURES_BROWN, False, "LIN+Bias", "FEATURES_BROWN"), name="BROWNGPjoinedfeaturesPooledLIN+Bias", 
                          RANDOM_RESTARTS=RANDOM_RESTARTS),
             #lambda: SVM("LIN", "BOWSVMLINjoinedfeaturesPooled", features=FEATURES_BOW),
             #lambda: SVM("LIN", "BROWNSVMLINjoinedfeaturesPooled", features=FEATURES_BROWN),
             
             #lambda: LR("BOWLRjoinedfeaturesPooled", features=FEATURES_BOW),
             #lambda: LR("BROWNLRjoinedfeaturesPooled", features=FEATURES_BROWN),
             
             #lambda: SklearnBaseline(lambda: DummyClassifier("most_frequent"), "MostFrequentPooled", [0]),
             
             #lambda: GPCONSTRUCTOR(kernel_constructor=lambda: single_task_kernel(ALLTEXTFEATURES, False, "LIN", "ALLFEATURES"), name="GPjoinedfeaturesPooled", 
             #                      RANDOM_RESTARTS=RANDOM_RESTARTS),
             
             #lambda: GPCONSTRUCTOR(kernel_constructor=lambda: singletask_summed(False, "LIN"), name="GPseparatedfeaturesPooled", 
             #             RANDOM_RESTARTS=RANDOM_RESTARTS),
             #lambda: GPCONSTRUCTOR(kernel_constructor=lambda: multi_task_kernel(tasks_number, index_task, singletask_summed(False, "LIN")), name="GPseparatedfeaturesICM", 
             #             RANDOM_RESTARTS=RANDOM_RESTARTS),
             #lambda: GPCONSTRUCTOR(kernel_constructor=lambda: multi_task_kernel(tasks_number, index_task, single_task_kernel(ALLTEXTFEATURES, False, "LIN", "ALLFEATURES")), 
             #                      name="GPjoinedfeaturesICM", RANDOM_RESTARTS=RANDOM_RESTARTS),
             #lambda: GPCONSTRUCTOR(kernel_constructor=lambda: multi_task_kernel(tasks_number, index_task, single_task_kernel(FEATURES_BOW, False, "LIN+Bias", "ALLFEATURES")), name="BOWGPjoinedfeaturesICM", 
             #             RANDOM_RESTARTS=RANDOM_RESTARTS),
             lambda: GPCONSTRUCTOR(kernel_constructor=lambda: multi_task_kernel(tasks_number, index_task, single_task_kernel(FEATURES_BROWN, False, "LIN+Bias", "FEATURES_BROWN")), 
                                   name="BROWNGPjoinedfeaturesICMLIN+Bias", RANDOM_RESTARTS=RANDOM_RESTARTS),
             lambda: GPCONSTRUCTOR(kernel_constructor=lambda: multi_task_kernel(tasks_number, index_task, single_task_kernel(FEATURES_BROWN, False, "LIN", "FEATURES_BROWN")), 
                                   name="BROWNGPjoinedfeaturesICMLIN", RANDOM_RESTARTS=RANDOM_RESTARTS),
             #lambda: GPCONSTRUCTOR(kernel_constructor=lambda: multi_task_kernel(tasks_number, index_task, single_task_kernel(FEATURES_BROWN, False, "LIN+Bias", "FEATURES_BROWN")), 
             #                      name="BROWNGPjoinedfeaturesICMLIN+Bias", RANDOM_RESTARTS=RANDOM_RESTARTS),
             lambda: GPCONSTRUCTOR(kernel_constructor=lambda: multi_task_kernel(tasks_number, index_task, single_task_kernel(FEATURES_BOW, False, "LIN", "FEATURES_BOW")), 
                                   name="BOWGPjoinedfeaturesICMLIN", RANDOM_RESTARTS=RANDOM_RESTARTS),
             #lambda: GPCONSTRUCTOR(kernel_constructor=lambda: multi_task_kernel(tasks_number, index_task, single_task_kernel(FEATURES_BOW, False, "LIN+Bias", "FEATURES_BOW")), 
             #                      name="BOWGPjoinedfeaturesICMLIN+Bias", RANDOM_RESTARTS=RANDOM_RESTARTS),
             lambda: GPCONSTRUCTOR(kernel_constructor=lambda: multi_task_kernel(tasks_number, index_task, single_task_kernel(ALLTEXTFEATURES, False, "LIN", "ALLTEXTFEATURES")), 
                                   name="ALLTEXTFEATURESGPjoinedfeaturesICMLIN", RANDOM_RESTARTS=RANDOM_RESTARTS),
             lambda: GPCONSTRUCTOR(kernel_constructor=lambda: multi_task_kernel(tasks_number, index_task, single_task_kernel(ALLFEATURES, False, "LIN", "ALLFEATURES")), 
                                   name="ALLFEATURESGPjoinedfeaturesICMLIN", RANDOM_RESTARTS=RANDOM_RESTARTS),
             #lambda: GPCONSTRUCTOR(kernel_constructor=lambda: multi_task_kernel(tasks_number, index_task, single_task_kernel(FEATURES_BOW, True, "LIN", "ALLFEATURES")), name="BOWARDGPjoinedfeaturesICM", 
             #             RANDOM_RESTARTS=RANDOM_RESTARTS),
             #lambda: GPCONSTRUCTOR(kernel_constructor=lambda: multi_task_kernel(tasks_number, index_task, single_task_kernel(FEATURES_BROWN, True, "LIN", "ALLFEATURES")), name="BROWNARDGPjoinedfeaturesICM", 
             #             RANDOM_RESTARTS=RANDOM_RESTARTS),
             #lambda: GPCONSTRUCTOR(kernel_constructor=lambda: multi_task_kernel(tasks_number, index_task, singletask_summed_BOW(False, "LIN")), name="BOWSIMPLEFEATSGPseparatedfeaturesICM", 
             #             RANDOM_RESTARTS=RANDOM_RESTARTS),
             
             #lambda: GPCONSTRUCTOR(kernel_constructor=lambda: multi_task_kernel(tasks_number, index_task, single_task_kernel(FEATURES_BROWN, True, "LIN", "FEATURES_BROWN")), 
             #                      name="BROWNARDPseparatedfeaturesICM", 
             #             RANDOM_RESTARTS=RANDOM_RESTARTS),
             #lambda: GPCONSTRUCTOR(kernel_constructor=lambda: multi_task_kernel(tasks_number, index_task, single_task_kernel(FEATURES_BOW, True, "LIN", "FEATURES_BOW")), 
             #                      name="BOWARDGPseparatedfeaturesICM", 
             #             RANDOM_RESTARTS=RANDOM_RESTARTS),
             ]
    return METHODS, map(lambda x: x().name, METHODS)

def get_methods_singletask(header, experimenttype, multiclass, RANDOM_RESTARTS=-1):
    if experimenttype=="old":
        #singletask_summed, _, ALLTEXTFEATURES, index_task=get_feature_indices_main_oldexperiments(header)
        print "[get_methods_multitask] OLD EXPERIMENT IS NOT IMPLEMENTED!!!"
    else:
        singletask_summed_BOW, singletask_summed_BROWN, singletask_summed_BOW_BROWN, ALLFEATURES, ALLTEXTFEATURES, FEATURES_BOW, FEATURES_BROWN, index_task=get_feature_indices_main(header)
    
    if multiclass:
        GPCONSTRUCTOR=lambda kernel_constructor, name, RANDOM_RESTARTS: MCGP(kernel_constructor=kernel_constructor, 
                                                                             labels=LABELS, name=name, RANDOM_RESTARTS=RANDOM_RESTARTS)
    else:
        GPCONSTRUCTOR=GPClassifier
        
    BOW_STR=lambda x: x[FEATURES_BOW]
    BROWN_STR=lambda x: x[FEATURES_BROWN]
        
    METHODS=[
             #lambda: SVM("LIN", "SVMLINjoinedfeatures", features=ALLTEXTFEATURES),
             lambda: SklearnBaseline(lambda: DummyClassifier("most_frequent"), "MostFrequent", []),
             lambda: GPCONSTRUCTOR(kernel_constructor=lambda: single_task_kernel(FEATURES_BOW, False, "LIN", "BOW"), name="BOWGPjoinedfeatures", 
                          RANDOM_RESTARTS=RANDOM_RESTARTS),
             lambda: GPCONSTRUCTOR(kernel_constructor=lambda: single_task_kernel(FEATURES_BROWN, False, "LIN", "BROWN"), name="BROWNGPjoinedfeatures", 
                          RANDOM_RESTARTS=RANDOM_RESTARTS),
             #lambda: GPCONSTRUCTOR(kernel_constructor=lambda: single_task_kernel(FEATURES_BOW, True, "LIN", "ALLFEATURES"), name="BOWARDGPjoinedfeatures", 
             #             RANDOM_RESTARTS=RANDOM_RESTARTS),
             #lambda: GPCONSTRUCTOR(kernel_constructor=lambda: single_task_kernel(FEATURES_BROWN, True, "LIN", "ALLFEATURES"), name="BROWNARDGPjoinedfeatures", 
             #             RANDOM_RESTARTS=RANDOM_RESTARTS),
             #lambda: GPCONSTRUCTOR(kernel_constructor=lambda: singletask_summed_BOW(False, "LIN"), name="BOWSIMPLEFEATSGPseparatedfeatures", 
             #             RANDOM_RESTARTS=RANDOM_RESTARTS),
             #lambda: GPCONSTRUCTOR(kernel_constructor=lambda: singletask_summed_BROWN(False, "LIN"), name="BROWNSIMPLEFEATSGPseparatedfeatures", 
             #             RANDOM_RESTARTS=RANDOM_RESTARTS),
             #lambda: GPCONSTRUCTOR(kernel_constructor=lambda: single_task_kernel(FEATURES_BOW, False, "LIN", "FEATURES_BOW")+single_task_kernel(FEATURES_BROWN, False, "LIN", "FEATURES_BROWN"), 
             #                      name="BROWN+BOWGPseparatedfeatures", RANDOM_RESTARTS=RANDOM_RESTARTS),
             ]
    return METHODS, map(lambda x: x().name, METHODS)


def get_allmethodnames():
    tasks_number=1
    header=[""]
    experimenttype="new"
    multiclass=False
    _, NAMES1 = get_methods_multitask(tasks_number, header, experimenttype, multiclass)
    _, NAMES2 = get_methods_singletask(header, experimenttype, multiclass)
    return NAMES1+NAMES2
