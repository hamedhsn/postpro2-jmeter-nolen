'''
Created on 15 Oct 2013

@author: hs302
'''
import matplotlib.pyplot as plt
import numpy as np

##############################################################################
def histreqstclient(intvl,type,filename,cliname,sername):
    clipath=filename
    f=open(clipath,'r')

    clilen=len(cliname.split('.'))
    serlen=len(sername.split('.'))
    #total time in millisec
    persecint=1000/intvl
    
    binstest=[]
    his=[]
    for i in range (1000/intvl):
        his.append(0)
   
    curtime=0
    realtime=0
    ftr = [3600,60,1]
    if (type=="cli2ser"):
        for line in f:
            l=line.rstrip().split(" ");
            if len(l)==1:
                break
            if str(l[8])=='5:46,' or str(l[8])=='1:30,':
                continue

            if len(l)>=20:
                if l[19]=="length" and (l[20] in ['54']) and ".".join(l[2].split(".")[0:clilen])==cliname:
                    timestr=l[0][:-7]
                    if curtime==0:
                        curtime=sum([a*b for a,b in zip(ftr, map(int,timestr.split(':')))])
                    if curtime!=sum([a*b for a,b in zip(ftr, map(int,timestr.split(':')))]):
                        curtime=sum([a*b for a,b in zip(ftr, map(int,timestr.split(':')))])
                        realtime+=1
                        for i in range (1000/intvl):
                            his.append(0)
                        if (realtime)*persecint==len(his):
                            break
                    his[int(realtime*persecint+(int(l[0][9:])/(intvl*1000)))]+=1                          
    else:
        for line in f:
            l=line.rstrip().split(" ");
            if len(l)>=20:
                if l[19]=="length" and (l[20] in ['29','1397']) and ".".join(l[2].split(".")[0:serlen])==sername:
                    timestr=l[0][:-7]
                    if curtime==0:
                        curtime=sum([a*b for a,b in zip(ftr, map(int,timestr.split(':')))])
                    if curtime!=sum([a*b for a,b in zip(ftr, map(int,timestr.split(':')))]):
                        curtime=sum([a*b for a,b in zip(ftr, map(int,timestr.split(':')))])
                        realtime+=1
                        for i in range (1000/intvl):
                            his.append(0)
                        if (realtime)*persecint==len(his):
                            break
                    his[int(realtime*persecint+(int(l[0][9:])/(intvl*1000)))]+=1                          
        
    
    print his,'\n'
    return his     
    print np.mean(his)
##############################################################################
def histreqstserver(intvl,type,filename,cliname,sername):
    clipath=filename
    f=open(clipath,'r')

    clilen=len(cliname.split('.'))
    serlen=len(sername.split('.'))
    #total time in milli sec
    persecint=1000/intvl
    
    binstest=[]
    his=[]
    for i in range (1000/intvl):
        his.append(0)
   
    curtime=0
    realtime=0
    ftr = [3600,60,1]
    if (type=="cli2ser"):
        for line in f:
            l=line.rstrip().split(" ");
            if len(l)==1:
                break
            if ".".join(l[2].split(".")[0:clilen])==cliname and l[5]=="P" and l[6]!="ack" and (str(l[6].split("(")[1][:-1]) in ['54']):
                timestr=l[0][:-7]
                if curtime==0:
                    curtime=sum([a*b for a,b in zip(ftr, map(int,timestr.split(':')))])
                if curtime!=sum([a*b for a,b in zip(ftr, map(int,timestr.split(':')))]):
                    curtime=sum([a*b for a,b in zip(ftr, map(int,timestr.split(':')))])
                    realtime+=1
                    for i in range (1000/intvl):
                            his.append(0)
                    if (realtime)*persecint==len(his):
                        break
                his[int(realtime*persecint+(int(l[0][9:])/(intvl*1000)))]+=1                          
    else:
        for line in f:
            l=line.rstrip().split(" ");
            if len(l)==1:
                break
            if ".".join(l[4].split(".")[0:clilen])==cliname and l[5]=="P" and l[6]!="ack" and (str(l[6].split("(")[1][:-1]) in ['29','1397']):
                #print "/n",l
                timestr=l[0][:-7]
                if curtime==0:
                    curtime=sum([a*b for a,b in zip(ftr, map(int,timestr.split(':')))])
                if curtime!=sum([a*b for a,b in zip(ftr, map(int,timestr.split(':')))]):
                    curtime=sum([a*b for a,b in zip(ftr, map(int,timestr.split(':')))])
                    realtime+=1
                    for i in range (1000/intvl):
                        his.append(0)
                    if (realtime)*persecint==len(his):
                        break
                his[int(realtime*persecint+(int(l[0][9:])/(intvl*1000)))]+=1                          
    
    print his,'\n',binstest,'\n'
    return his
    print np.mean(his)
##############################################################################
def plt_traf_hist(fipath,finame,his,intvl,title,xlbl,ylbl):
    bins=[]
    for i in range(len(his)):
        bins.append((i+1)*intvl)
    plt.bar(bins,his,width=intvl-0.1*intvl)
    plt.xticks(range(min(bins),max(bins),20000),range(0,max(bins)/1000,20))
    plt.xticks(rotation=90)
    #plt.xlim(0,120000)
    
    plt.xlabel(xlbl)
    plt.ylabel(ylbl[:-4]+str(intvl)+ ylbl[-5:])
    
    #title
    plt.title(title)
    plt.yticks(range(0,max(his)+10,20))
    plt.ylim(0,int(np.mean(his)*2))
    #plt.xticks(30)

    #plt.get_current_fig_manager().window.state('zoomed')
    plt.grid()
    
    figure = plt.gcf() # get current figure
    figure.set_size_inches(18.5,10.5 )
    figure.savefig(fipath[:-4]+finame)

    
    plt.show()  
    print "bins",bins                  
##############################################################################
'''plot all 4 send and receive traffic graphs in one'''
def plt_traf_sndrecv(fipath,finame,intvl,his11,his12,his21,his22):

# print np.mean(h11),np.mean(h12),np.mean(h21),np.mean(h22)
# print np.std(h11),np.std(h12),np.std(h21),np.std(h22)
    bins=[]
    minlen=min(len(his11),len(his12),len(his21),len(his22))
    '''fill out the bins 1000,2000,3000,... msec'''
    for i in range(minlen):
        bins.append((i+1)*intvl)

    '''remove all the extra numbers from the end of the hisxx lists'''
    print minlen,len(his11),len(his12),len(his21),len(his22)
    for i in range(len(his11)-minlen):
        his11.pop(i-1)
    for i in range(len(his12)-minlen):
        his12.pop(i-1)
    for i in range(len(his21)-minlen):
        his21.pop(i-1)
    for i in range(len(his22)-minlen):
        his22.pop(i-1)

            
    f,axarr = plt.subplots(2, 2)
    #plt.setp(axarr, xticks=[0.1, 0.5, 0.9], xticklabels=['a', 'b', 'c'],yticks=[1, 2, 3])
    axarr[0, 0].bar(bins,his11,width=intvl-0.1*intvl)
    axarr[0, 0].set_title('Client requests(client side)')
    #axarr[0, 0].set_xticklabels(range(0,max(bin11)/1000,10))
    axarr[0,0].set_ylabel("Histogram(every 1000 milisec)")
#     axarr[0, 0].set_xticks(range(0,max(bins),10000))
     
    axarr[0, 1].bar(bins,his12,width=intvl-0.1*intvl)
    axarr[0, 1].set_title('Client requests(server side)')
#     axarr[0, 1].set_xticks(range(0,max(bin),10000))
     
    axarr[1, 0].bar(bins,his21,width=intvl-0.1*intvl)
    axarr[1, 0].set_title('Server Response(Client side)')
#     axarr[1, 0].set_xticks(range(0,max(bins),10000))
    #axarr[1, 0].set_xticklabels(range(0,max(bin12)/1000,10))
     
    axarr[1, 1].bar(bins,his22,width=intvl-0.1*intvl)
    axarr[1, 1].set_title('Server Response(server side)')
#     axarr[1, 1].set_xticks(range(0,max(bins),10000))
    axarr[1, 0].set_xlabel("Sec") 
     
    # plt.setp([a.get_xticklabels() for a in axarr[0, :]], visible=False)
    # plt.setp([a.get_yticklabels() for a in axarr[:, 1]], visible=False)

    #plt.get_current_fig_manager().window.state('zoomed')
    plt.grid()
    figure = plt.gcf() # get current figure
    figure.set_size_inches(18.5,10.5 )
    #figure.savefig('F:\\Dropbox\\Dropbox\\Reading Stuff\\0-MyPhD\\2exp-tcpdump\\qmul\\sg\\3sg5th20e20.png')
    figure.savefig(fipath[:-4]+finame)

    

    plt.show()