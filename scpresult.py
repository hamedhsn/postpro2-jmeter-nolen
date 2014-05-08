'''
Created on 7 Oct 2013

@author: hs302
'''
from fileinput import filename
''' Copy back the result of the experiment '''
import os


node2becopied1=[]#client nodes
node2becopied2=[]#server nodes
fr=open('/homes/hs302/workspace/casstcpdump/src/postpro1-ycsb/prop.txt','r')
lines = fr.readlines()
for line in lines:
    l=line.rstrip().split("=");
    if l[0]=='client':
        node2becopied1.append(l[1].split(","))
    elif l[0]=='hosts':
        node2becopied2.append(l[1].split(","))
    elif l[0]=='filname':
        filname=l[1]

        
'''copy back all the tar file - extract them and remove the tar file'''        
path="/homes/hs302/Dropbox/Reading\ Stuff/0-MyPhD/2exp-tcpdump/5qmul/new/"
for node in node2becopied1:
    os.system('scp -i ~/.ssh/id_rsa qmulple_hsn_test_cloud@'+str(node)[2:][:-2]+':TEST/res/'+filname+'cli.tar '+path)
    os.system("tar -zxvf "+path+filname+"cli.tar" " -C "+path) 
for node in node2becopied2:
    os.system('scp -i ~/.ssh/id_rsa qmulple_hsn_test_cloud@'+str(node)[2:][:-2]+':TEST/res/'+filname+'ser.tar '+path)
    os.system("tar -zxvf "+path+filname+"ser.tar" " -C "+path)
os.system("rm "+path+"*.tar")






# serverfilePath = "TCPDUMP/sg/1sg5th20e30sg.txt"
# server = "planetlab1.comp.nus.edu.sg"
# pyserpath="/homes/hs302/Dropbox/Reading\ Stuff/0-MyPhD/2exp-tcpdump/qmul/sg/"
# path1="scp -i ~/.ssh/id_rsa qmulple_hsn_test_cloud@"+server+":"+serverfilePath+" "+pyserpath
# os.system(path1)
#   
# # serverfilePath = "casstcpdump/cassoverload/itchyserdmp3gen18.txt"
# # server = "planetlab02.sys.virginia.edu"
# # pyserpath="/homes/hs302/Dropbox/Reading\ Stuff/0-MyPhD/2exp-tcpdump/4over/itchyserdmp3gen18.txt"
# # path1="scp -i ~/.ssh/id_rsa qmulple_hsn_test_cloud@"+server+":"+serverfilePath+" "+pyserpath
# # os.system(path1)  
# 
# clientfilePath = "TCPDUMP/sg/1sg5th20e30qm.txt"
# client = "planetlab1.nrl.eecs.qmul.ac.uk"
# pyclipath="/homes/hs302/Dropbox/Reading\ Stuff/0-MyPhD/2exp-tcpdump/qmul/sg/"
# path="scp -i ~/.ssh/ qmulple_hsn_test_cloud@"+client+":"+clientfilePath+" "+pyclipath
# os.system(path)
# 
# # serverfilePath = "tcpdmptraffic/itchyclidmp3gen18.txt"
# # server = "itchy.comlab.bth.se"
# # pyserpath="/homes/hs302/Dropbox/Reading\ Stuff/0-MyPhD/2exp-tcpdump/itchy-client-tcpdmptraffic/itchyclidmp3gen18.txt"
# # path1="scp -i ~/.ssh/id_rsa qmulple_hsn_test_cloud@"+server+":"+serverfilePath+" "+pyserpath
# os.system(path1)

