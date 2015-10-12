'''
Created on 6 Oct 2015

@author: michal
'''
import numpy as np

def summarize_kernel(kmat, y_train, y_test, indices_train, indices_test, header, method, X_test):
    print "[summarize_kernel] START", header
    for i in xrange(kmat.shape[0]):
        for j in xrange(i, kmat.shape[1]):
            print indices_train[i], indices_test[j], int(y_train[i][0]), int(y_test[j][0]),\
            (1.0*kmat[i, j])/np.sum(kmat[:, j]), kmat[i, j], np.sum(kmat[:, j]), method.predict_vector(X_test[j:j+1,:])[0]
    print "[summarize_kernel] END"

def print_mcgp_method(method, header):
    try:
        print method.models
        for key, method in method.models.items():
            print "[print_mcgp_method] GP for label:", key
            try:
                print "[print_mcgp_method] method.k:", method.kern
                
                try:
                    print "add.linear.variances:"
                    for features in ['FEATURES_BOW', 'FEATURES_BROWN', 'FEATURES_EMOTICON']:
                        try:
                            print "Features:", features
                            weight_pairs=[]
                            for ind, active_dim in enumerate(getattr(method.kern, features).active_dims):
                                try:
                                    weight_pairs.append((header[active_dim], getattr(method.kern, features)[ind]))
                                except:
                                    break
                            weight_pairs=sorted(weight_pairs, key=lambda x: x[1], reverse=True)
                            for a, b in weight_pairs:
                                print a+": ", b
                        except:
                            pass
                except:
                    print "[print_mcgp_method] couldn't print add.linear.variances"
                
                try:
                    try:
                        print "B:", method.kern.parts[1].B
                    except:
                        print "B:", method.kern.parts[0].parts[1].B
                except:
                    print "B:", method.kern.parts[0].parts[0].parts[1].B
            except:
                print "[Experiment.evaluate_method] couldn't print method.k."
    except:
        print "[Experiment.evaluate_method] couldn't print method.k."