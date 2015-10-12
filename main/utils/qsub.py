'''
Created on 23 Mar 2015

@author: Zsolt, michal

Thanks to Zsolt Bitvai for idea and code.
'''
import sys
import socket
from subprocess import Popen, PIPE, STDOUT
import time
import os
from main.utils.utils import make_dir, current_time_str
import random
class Qsub(object):
    '''
    Class for submitting jobs to a server. 
    '''
    
    QSUB_HEADER_EASY="\n".join(["#!/bin/bash",
                           "#$ -m a",
                           "#$ -M acp13ml@sheffield.ac.uk"
                           "$ -l h_rt=6:00:00",
                           "#$ -o result.log",
                           "#$ -j y",
                           "#$-l mem=10G", 
                           "#$-l rmem=10G"])
    
    QSUB_HEADER_EASY_LONG="\n".join(["#!/bin/bash",
                           "#$ -m a",
                           "#$ -M acp13ml@sheffield.ac.uk"
                           "$ -l h_rt=16:00:00",
                           "#$ -o result.log",
                           "#$ -j y",
                           "#$-l mem=10G", 
                           "#$-l rmem=10G"])
    
    QSUB_HEADER_HARD="\n".join(["#!/bin/bash",
                           "#$ -m a",
                           "#$ -M acp13ml@sheffield.ac.uk"
                           "$ -l h_rt=12:00:00",
                           "#$ -o result.log",
                           "#$ -j y",
                           "#$-l mem=40G", 
                           "#$-l rmem=30G"])

    QSUB_HEADER_MOREHARD="\n".join(["#!/bin/bash",
                           "#$ -m a",
                           "#$ -M acp13ml@sheffield.ac.uk"
                           "$ -l h_rt=12:00:00",
                           "#$ -o result.log",
                           "#$ -j y",
                           "#$-l mem=60G", 
                           "#$-l rmem=40G"])
    script_name="tmp.sh"
    SUBM_TIMEOUT = 0.02
    WAIT_TIMEOUT = 1
    WAIT_FREQ = 20
    #RESULTS_CAT = "results"
        
    if 'iceberg' in socket.gethostname():
        SUB_CMD="qsub {}"
        MAX_WORKERS = 1999#350
        WORKER_CMD = "Qstat"
        USERNAME="acp13ml"
        RESULTS_CAT = "results"#"/fastdata/acp13ml"
        RUN_FOREGROUND=True
    elif 'yarra' in socket.gethostname():
        SUB_CMD="sh {} &"
        MAX_WORKERS = 30
        WORKER_CMD = "ps"
        USERNAME="\n"
        RESULTS_CAT = "results"
        RUN_FOREGROUND=False
    else:
        print "[Qsub] Unknown host: just printing out the script content!"
        SUB_CMD="cat {}"
        MAX_WORKERS = 999999
        WORKER_CMD = "ps"
        USERNAME="\n"
        RESULTS_CAT = "results"
        RUN_FOREGROUND=True
    
    def __init__(self, CVFOLDS, methodnames, pyscript, global_parameters, outcat_prefix, train_set_ratios, experimenttype):
        print "[Qsub.__init__]"
        self.cnt = 0
        self.CVFOLDS=CVFOLDS
        self.methodnames=methodnames
        self.pyscript=pyscript
        self.global_parameters=map(str, global_parameters)
        self.create_res_catalogue(outcat_prefix)
        
        if experimenttype=="easy":
            self.QSUB_HEADER=self.QSUB_HEADER_EASY
        elif experimenttype=="hard":
            self.QSUB_HEADER=self.QSUB_HEADER_HARD
        elif experimenttype=="easylong":
            self.QSUB_HEADER=self.QSUB_HEADER_EASY_LONG
        elif experimenttype=="morehard":
            self.QSUB_HEADER=self.QSUB_HEADER_MOREHARD
        else:
            print "Wrong experimenttype:", experimenttype, "!!!"
        
        self.train_set_ratios=train_set_ratios
         
    def create_res_catalogue(self, outcat_prefix):
        self.outcat=os.path.join(self.RESULTS_CAT, outcat_prefix+("_".join(self.global_parameters)).replace("/", "").replace(".", ""))
        make_dir(self.outcat)
         
    def iterate_settings(self, actions):
        for foldrun in xrange(self.CVFOLDS):
            for methodname in self.methodnames:
                for train_set_ratio in self.train_set_ratios:
                    for action in actions:
                        action(map(str, [foldrun, methodname, train_set_ratio]))
        
    def inc_count(self, run_parameters):
        self.cnt+=1
    
    def create_qsub_script(self, run_parameters):
        #create script
        with open(self.script_name, 'w') as f:
            f.write(self.QSUB_HEADER+"\n")
            res_fname=os.path.join(self.outcat,"_".join(run_parameters))
            
            f.write(" ".join(["python", self.pyscript]+run_parameters+self.global_parameters+[">"]+[res_fname]))
    
    def submit_qsub_script(self, run_parameters):
        print self._execute(self.SUB_CMD.format(self.script_name))
    
    def print_progress_bar(self, run_parameters):
        print "/".join(map(str, [self.cnt, self.all_terations]))
        
    def _execute(self, cmd):
        if self.RUN_FOREGROUND:
            outp = Popen(cmd, shell=True, stdin=PIPE, stdout=PIPE, stderr=STDOUT).communicate()[0]
        else:
            #print cmd.split()
            outp = Popen(cmd.split(), stdin=PIPE, stderr=STDOUT)#.communicate()[0]
        time.sleep(self.SUBM_TIMEOUT)
        return outp
            
    def get_running_workers(self):
        output = Popen(self.WORKER_CMD, shell=True, stdin=PIPE, stdout=PIPE, stderr=STDOUT).communicate()[0]
        return output.count(self.USERNAME)
        
    def wait(self):
        while self.get_running_workers() > self.MAX_WORKERS:
            print "max workers exceeded, wating..."
            time.sleep(self.WAIT_TIMEOUT)
            
    def wait_condition(self, run_parameters):
        if self.cnt % self.WAIT_FREQ == 0:
            self.wait()
    
    def run(self):
        print "[Qsub.run]"
        self.iterate_settings([self.inc_count])
        self.all_terations = self.cnt
        print "Iterations to run:", self.all_terations
        
        self.cnt=0
        self.iterate_settings([self.create_qsub_script, self.submit_qsub_script, self.inc_count, self.print_progress_bar, self.wait_condition])
