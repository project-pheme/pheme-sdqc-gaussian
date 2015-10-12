'''
Created on 2 Jun 2015

@author: michal
'''
from main.models.kernels import single_task_kernel

def extract_feature_indices(header):
    FEATURES_BOW=[ind for ind, name in enumerate(header) if name.startswith("BOW_")]
    FEATURES_BOWBI=[ind for ind, name in enumerate(header) if name.startswith("BOWBI_")]
    
    FEATURES_BROWN=[ind for ind, name in enumerate(header) if name.startswith("BROWN_")]
    FEATURES_BROWNBI=[ind for ind, name in enumerate(header) if name.startswith("BROWNBI_")]
    
    FEATURES_EMOTICON=[ind for ind, name in enumerate(header) if name.startswith("EMOTICONS_")]
    FEATURES_PUNCT=[ind for ind, name in enumerate(header) if name.startswith("PUNCT_")]
    FEATURES_HASHTAG=[ind for ind, name in enumerate(header) if name.startswith("HASHTAG_")]
    FEATURES_URL=[ind for ind, name in enumerate(header) if name.startswith("URL_")]
    FEATURES_USR=[ind for ind, name in enumerate(header) if name.startswith("USR_")]
    
    FEATURES_TIME=[ind for ind, name in enumerate(header) if name=="time"]
    FEATURES_RTSIMPLE=[ind for ind, name in enumerate(header) if name=="is_simple_retweet"]
    FEATURES_RTCOMPLEX=[ind for ind, name in enumerate(header) if name=="is_complex_retweet"]
    FEATURES_RT=[ind for ind, name in enumerate(header) if name=="is_retweet"]
    index_task=[ind for ind, name in enumerate(header) if name=="event"]
    
    return FEATURES_BOW, FEATURES_BOWBI, FEATURES_BROWN, FEATURES_BROWNBI, FEATURES_EMOTICON,\
            FEATURES_PUNCT, FEATURES_HASHTAG, FEATURES_URL, FEATURES_TIME, FEATURES_USR, FEATURES_RTSIMPLE, FEATURES_RTCOMPLEX, FEATURES_RT, index_task
    
def get_feature_indices_main(header):
    FEATURES_BOW, FEATURES_BOWBI, FEATURES_BROWN, FEATURES_BROWNBI, FEATURES_EMOTICON,\
    FEATURES_PUNCT, FEATURES_HASHTAG, FEATURES_URL, FEATURES_TIME, FEATURES_USR, FEATURES_RTSIMPLE, FEATURES_RTCOMPLEX, FEATURES_RT, index_task=extract_feature_indices(header)
    
    singletask_summed_BOW=lambda ARD, ktype: single_task_kernel(FEATURES_BOW, ARD, ktype, "BOWUNI")+\
                                        single_task_kernel(FEATURES_EMOTICON, ARD, ktype, "EMOTICON")+\
                                        single_task_kernel(FEATURES_HASHTAG, ARD, ktype, "HASHTAG")+\
                                        single_task_kernel(FEATURES_USR, ARD, ktype, "USR")+\
                                        single_task_kernel(FEATURES_URL, ARD, ktype, "URL")+\
                                        single_task_kernel(FEATURES_RT, ARD, ktype, "RT")
                                        #single_task_kernel(FEATURES_BOWBI, ARD, ktype, "BOWBI")+\
                                        #single_task_kernel(FEATURES_BROWN, ARD, ktype, "BROWNUNI")+\
                                        #single_task_kernel(FEATURES_BROWNBI, ARD, ktype, "BROWNBI")+\
                                        #single_task_kernel(FEATURES_TIME, ARD, "RBF", "TIME")+\
                                        
    singletask_summed_BROWN=lambda ARD, ktype: single_task_kernel(FEATURES_BOW, ARD, ktype, "BOWUNI")+\
                                        single_task_kernel(FEATURES_BROWN, ARD, ktype, "BROWNUNI")+\
                                        single_task_kernel(FEATURES_EMOTICON, ARD, ktype, "EMOTICON")+\
                                        single_task_kernel(FEATURES_HASHTAG, ARD, ktype, "HASHTAG")+\
                                        single_task_kernel(FEATURES_USR, ARD, ktype, "USR")+\
                                        single_task_kernel(FEATURES_URL, ARD, ktype, "URL")+\
                                        single_task_kernel(FEATURES_RT, ARD, ktype, "RT")
                                        #single_task_kernel(FEATURES_BOWBI, ARD, ktype, "BOWBI")+\
                                        #single_task_kernel(FEATURES_TIME, ARD, "RBF", "TIME")+\
                                        #single_task_kernel(FEATURES_BROWNBI, ARD, ktype, "BROWNBI")+\
    
    
    singletask_summed_BOW_BROWN=lambda ARD, ktype: single_task_kernel(FEATURES_BOW, ARD, ktype, "BOWUNI")+\
                                        single_task_kernel(FEATURES_BROWN, ARD, ktype, "BROWNUNI")+\
                                        single_task_kernel(FEATURES_EMOTICON, ARD, ktype, "EMOTICON")+\
                                        single_task_kernel(FEATURES_HASHTAG, ARD, ktype, "HASHTAG")+\
                                        single_task_kernel(FEATURES_USR, ARD, ktype, "USR")+\
                                        single_task_kernel(FEATURES_URL, ARD, ktype, "URL")+\
                                        single_task_kernel(FEATURES_RT, ARD, ktype, "RT")
                                        #single_task_kernel(FEATURES_BOWBI, ARD, ktype, "BOWBI")+\
                                        #single_task_kernel(FEATURES_TIME, ARD, "RBF", "TIME")+\
                                        #single_task_kernel(FEATURES_BROWNBI, ARD, ktype, "BROWNBI")+\
    
    #ALLFEATURES=reduce(lambda x, y: x+y, [FEATURES_BOW, FEATURES_BOWBI, FEATURES_BROWN, FEATURES_BROWNBI, FEATURES_EMOTICON,\
    #                                      FEATURES_PUNCT, FEATURES_HASHTAG, FEATURES_URL, FEATURES_TIME, FEATURES_USR, FEATURES_RTSIMPLE, 
    #                                      FEATURES_RTCOMPLEX, FEATURES_RT, index_task])
    ALLFEATURES=reduce(lambda x, y: x+y, [FEATURES_BOW, FEATURES_BROWN, FEATURES_EMOTICON,\
                                          FEATURES_PUNCT, FEATURES_HASHTAG, FEATURES_URL, FEATURES_USR,
                                          FEATURES_RT])
    
    ALLTEXTFEATURES=reduce(lambda x, y: x+y, [FEATURES_BOW, FEATURES_BROWN, FEATURES_EMOTICON,\
                                              FEATURES_PUNCT, FEATURES_HASHTAG, FEATURES_URL])
    
    return singletask_summed_BOW, singletask_summed_BROWN, singletask_summed_BOW_BROWN, ALLFEATURES, ALLTEXTFEATURES, FEATURES_BOW, FEATURES_BROWN, index_task

def get_feature_indices_main_oldexperiments(header):
    FEATURES_BOW=[ind for ind, name in enumerate(header) if name.startswith("BOW_")]
    FEATURES_SPECTRAL=[ind for ind, name in enumerate(header) if name.startswith("spectral_components_")]
    textfeatures=FEATURES_BOW+FEATURES_SPECTRAL
    index_task=[ind for ind, name in enumerate(header) if name=="dataset"]
    singletask_summed=lambda ARD, ktype: single_task_kernel(FEATURES_BOW, ARD, ktype, "BOW")+\
                                        single_task_kernel(FEATURES_SPECTRAL, ARD, ktype, "SPECTRAL")
    return singletask_summed, textfeatures, textfeatures, index_task
