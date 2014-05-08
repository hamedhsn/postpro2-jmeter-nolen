'''
Created on 23 Oct 2013

@author: hs302
'''
import matplotlib.pyplot as plt
from pylab import *
from numpy.random import normal 
import numpy as np
#################################################
def plot(fipath,finame,rec,time,cliorser):
    x=[]
    
    sec=int(time[0])
    for i in range(len(time)):
        time[i]=round((time[i]-sec),1)
        #print x
    print "time:",time
    print "rec:",rec
    b1,=plt.plot(time, rec, color='blue', linestyle='dashed', marker='s', markerfacecolor='blue', markersize=4)
    
    #configure  X axes
#     plt.xticks(range(0,int(max(time)),60))
#     plt.xticks(rotation=90)
#     plt.xlim(0,120)
#     
#     #configure  Y axes
#     plt.yticks(np.arange(0, max(rec)+1, 100))
#     plt.ylim(0,5000)
    
    #labels
    plt.xlabel("Time(sec)")
    plt.ylabel("Latency(MilliSecond)")
    
    
    #title
    if cliorser=='cli':
        plt.title("Cassandra operation latency (client-->server)")
    else:
        plt.title("Server side Latency (client-->server)")
 
    #plt.get_current_fig_manager().window.state('zoomed')
    plt.grid()
    figure = plt.gcf() # get current figure
    figure.set_size_inches(18.5,10.5 )
    #figure.savefig('F:\\Dropbox\\Dropbox\\Reading Stuff\\0-MyPhD\\2exp-tcpdump\\qmul\\sg\\3sg5th20e20.png')
    figure.savefig(fipath[:-4]+finame)

    plt.show()
##############################################################################
''' Plot the throughput and latency in the same plot'''
def plt_serv_lat_thput_1axis(fipath,finame,his,serfilepath,intvl,rec,time,grintvl):

    bins=[]
    #for i in range(min(len(his12),len(his22))):
        #his.append(his12[i]-his22[i])
    for i in range(len(his)):
        bins.append((i+1)*intvl)
#     print "h12",h12
#     print "h22",h22
#     print "difference",his
#     bins=bin12
    sec=int(time[0])
    for i in range(len(time)):
        time[i]=round((time[i]-sec),1)

    fi=0
    la=0
    mx=int(max(time))
    rpt=0
    while fi<mx:
        rpt+=1 
        t=[]
        b=[]
        r=[]
        h=[]
        la+=grintvl

        for i in range(fi,la):
            b.append(bins[i])
            h.append(his[i]*1)
        
        tiatt=[]
        for i in range(len(time)):
            if time[i]>=fi and time[i]<la:
                tiatt.append(i)
                t.append(time[i]*intvl)
    
        for i in (tiatt):
            r.append(rec[i])
     
        print "time:",len(t),t
        print "r:",len(r),r
        print "bintime:",len(b),b
        print "h:",len(h),h
         
        p=plt.bar(b,h,width=intvl-0.1*intvl)        
        b1,=plt.plot(t, r, color='red', linestyle='dashed', marker='s', markerfacecolor='red', markersize=4)
     
        plt.xlabel("Time(msec)")
        plt.ylabel("Throughput & Latency(msec)")
     
        #plt.get_current_fig_manager().window.state('zoomed')
        plt.grid()
        figure = plt.gcf() # get current figure
        figure.set_size_inches(18.5,10.5 )
#         figure.savefig(fipath[:-4]+finame+str(rpt))
     
        plt.show()
    
        fi+=grintvl
##############################################################################
##############################################################################

'''receives the string in hr:min:sec.microsec and convert it to second.microsecond
'''
def timeconv(str):
    ftr = [3600,60,1]
    sec=0
    sec=sum([a*b for a,b in zip(ftr, map(int,str[:-7].split(':')))])
    
    sec+=float(str.split('.')[1])/1000000
    return sec
#########################################################################################
def timeseries(thr,path):
    clipath=path
    f=open(clipath,'r')
    prev=0
    tmplistmili=[]
    tmp=[]
    for line in f:
        l=line.lower().rstrip().split(" ");
        if len(l)==1:
            break

        if len(l)>=20:
            if l[19]=="length" and (l[20] in ['54']) and l[2]=="planetlab1.nrl.eecs.qmul.ac.uk."+thr:
                if len(tmp)==0:
                    tmp.append(timeconv(l[0]))
                    continue
                
                #tmp.append(prev)
                tmp.append(timeconv(l[0])-tmp[0])
                tmplistmili.append(tmp)
                #print tmp
                tmp=[]
                tmp.append(timeconv(l[0]))
#                 if int(nn)%10==0:
#                     tmplist.append(0)

    print "tmplistmili:",tmplistmili
    
    x=[]
    data=[]
    
    for i in range(len(tmplistmili)):
        x.append(round((tmplistmili[i][0]-tmplistmili[0][0]),1))
        data.append(tmplistmili[i][1]*1000)
    #plot(data, x, "ser")
    print "\ndata",data
    b1,=plt.plot(x, data, color='red', linestyle='dashed', marker='s', markerfacecolor='red', markersize=4)
    
    #configure  X axes
    #     plt.xticks([1,2,3,4])
#    plt.xticks(np.arange(0, max(x), 60),np.arange(0, max(x), 60))
    #plt.xticks([x for x in binstest],[x/1000 for x in binstest])
    plt.xticks(rotation=90)
    #plt.xlim(0,100)
#     binstest=[]
#     tottime=1320000
#     for i in range((tottime/120000)):
#         binstest.append((i+1)*120000)
#     print binstest
#     plt.xticks([x for x in binstest],[x/1000 for x in binstest])
    plt.xticks(rotation=90)
    
    
    #configure  Y axes
    
    #plt.yticks([20, 21, 20.5, 20.8])
    plt.yticks(np.arange(0, max(data)+1, 50))
    plt.ylim(0,3000)
    
    #labels
    plt.xlabel("Time(sec)")
    plt.ylabel("Latency(MilliSecond)")
    
    
    #title
    plt.title("Time series of the intervals")
    
    # Save the figure in a separate file
#     plt.savefig('sine_function_plain.png')
    
#     plt.legend('dkadkakadak')
    #plt.legend( [b1], ["Cassandra Server Side Latency Behavior"])
    # Draw the plot to the screen
    plt.grid()
    plt.show()
    
    
    
#################################################################################
''' calculating the cassandra latency based on the outgoing and incoming tcpdump traffic per thread'''
def thr_cli_lat(path,cliname,sername,thr1):

    clipathname=path
    clilen=len(cliname.split('.'))
    serlen=len(sername.split('.'))
    
    f=open(clipathname,'r')
    clirecord=[]
    tmprec={}
    if len(thr1)==0:
#         threads=[]  #
        only1thr=False
    else:
        tmprec[str(thr1[0])]=['0','0','0','0','0','0']
#         threads=thr1 #
        only1thr=True

#     records=[]#
#     opthr=[]#
#     tmp=[]#
#     repcheck=[]#
    flag=0
    for line in f:
        l=line.lower().rstrip().split(" ");
        if len(l)==1:
            break
        if len(l)<19:
            continue
        if l[6]=='[s.],' or l[6]=='[s],':
            continue

#         if l[0]=='21:06:15.690901':
#             print 'sd'
        if ".".join(l[4].split(".")[0:clilen])==cliname and l[4].split('.')[-1][:-1] not in tmprec.keys() and only1thr==False:
            tmprec[l[4].split(".")[-1][:-1]]=['0','0','0','0','0','0']
            #threads.append(l[4].split(".")[-1][:-1])#
        if ".".join(l[2].split(".")[0:clilen])==cliname and l[2].split('.')[-1] not in tmprec.keys() and only1thr==False:
            tmprec[l[2].split(".")[-1]]=['0','0','0','0','0','0']
            #threads.append(l[2].split(".")[-1])#
        
        #ignor the first packet cli->ser=seq5:46 and ser->cli=seq1:30
#         if str(l[8])=='5:46,' or str(l[8])=='1:30,':
        
        if int(l[8][:-1].split(":")[0])<10:
            continue
        
        #find the Cassandra latency from client trace
        

        if ".".join(l[2].split(".")[0:clilen])==cliname and l[7]=="seq" and l[9]=="ack" and l[2].split(".")[-1] in tmprec.keys():
            thr=l[2].split(".")[-1]
            seq=l[8][:-1]
            
            if tmprec[thr][1]!=seq:
#                 if int(tmprec[thr][5])==0:
#                     print "drop"
                if tmprec[thr][0]!='0' and int(tmprec[thr][5])!=0 : 
#                     print l                                #check weather  it is not the firstrecord
                    tmp=[]                                              #then add thread no,Start time,End time, Duration
                    tmp.append(thr)
                    tmp.append(tmprec[thr][2])
                    tmp.append(tmprec[thr][5])
                    tmp.append(round((tmp[2]-tmp[1]),6))
                    clirecord.append(tmp)
                    tmprec[thr][3]='0'
                    tmprec[thr][4]='0'
                    tmprec[thr][5]='0'
                tmprec[thr][0]=l[10][:-1]                               #add ack no
                tmprec[thr][1]=l[8][:-1]                                #add seq no
                tmprec[thr][2]=timeconv(l[0])                           #add send time
            
            
            
#             
#             tmp=[]#
#             tmp.append(l[2].split('.')[-1])#
#             tmp.append(l[8][:-1])#
#             tmp.append(timeconv(l[0]))#
#             
#             for m in range(len(repcheck)):
#                 if repcheck[m][0]==tmp[0]:
#                     if repcheck[m][1]==tmp[1]:
#                         flag=1
#                         break
#                     
#             for th in opthr:
#                 if tmp[0]==th[0] and tmp[1]==th[1]:
#                     flag=1
#                     break  
#             if flag==0:
#                 opthr.append(tmp)
#                 #adding the port and seq number to repcheck
#                 for m in range(len(repcheck)):
#                     if repcheck[m][0]==tmp[0]:
#                         repcheck[m][1]=tmp[1]
#                         fl=1
#                         break
#                 if fl==0:
#                     repcheck.append([tmp[0],tmp[1]])
#             else:
#                 flag=0    
#             continue
        elif ".".join(l[4].split(".")[0:clilen])==cliname and l[7]=="seq" and l[9]=="ack" and l[4].split(".")[-1][:-1] in tmprec.keys():
#             print l
#             if l[0]=='21:05:15.666537':
#                 print l[10][:-1]
            if tmprec[l[4].split(".")[-1][:-1]][0]!='0' and tmprec[l[4].split(".")[-1][:-1]][1].split(":")[1]==l[10][:-1] :                          
                tmprec[l[4].split(".")[-1][:-1]][3]=l[10][:-1]          #add ack no
                tmprec[l[4].split(".")[-1][:-1]][4]=l[8][:-1]           #add seq no
                tmprec[l[4].split(".")[-1][:-1]][5]=timeconv(l[0])      #add receieve time
                
                       
#             port=l[4].split('.')[-1][:-1]
#             for x in opthr:
#                 if x[0]==port:
#                     tmp=[]
#                     tmp=x
#                     tmp.append(timeconv(l[0]))
#                     tmp.append(round((tmp[3]-tmp[2]),6))
#                     opthr.remove(x)
#                     #print tmp
#                     records.append(tmp)
# 
#                     break
            

    #print threads
    return clirecord,tmprec.keys()
#########################################################################################
''' calculating the server side latency based on the outgoing and incoming tcpdump traffic per thread'''
def thr_serv_lat(path,cliname,sername,thr1):

    clipathname=path
    clilen=len(cliname.split('.'))
    serlen=len(sername.split('.'))
    
    f=open(clipathname,'r')
    serrecord=[]
    tmprec={}
    if len(thr1)==0:
        only1thr=False
    else:
        tmprec[str(thr1[0])]=['0','0','0','0','0','0']
        only1thr=True

    if f.readline().lower().rstrip().split(" ")[5]!='flags':
        for line in f:
            l=line.lower().rstrip().split(" ");
            if len(l)==1:
                break
            if len(l)<13 or str(l[6][-1])!=')':
                continue
            if l[5]=='s' or l[5]=='s.':
                continue

    
            if ".".join(l[4].split(".")[0:clilen])==cliname and l[4].split('.')[-1][:-1] not in tmprec.keys() and only1thr==False:
                tmprec[l[4].split(".")[-1][:-1]]=['0','0','0','0','0','0']
            if ".".join(l[2].split(".")[0:clilen])==cliname and l[2].split('.')[-1] not in tmprec.keys() and only1thr==False:
                tmprec[l[2].split(".")[-1]]=['0','0','0','0','0','0']
            
            #ignor the first packet cli->ser=seq5:46 and ser->cli=seq1:30
    #         if str(l[6])=='5:46(41)' or str(l[6])=='1:30(29)':
    #             continue
            if int(l[6].split("(")[0].split(":")[0])<10:
                continue
            
            #find the Server side latency 
            if ".".join(l[2].split(".")[0:clilen])==cliname and l[7]=="ack" and l[2].split(".")[-1] in tmprec.keys():
                thr=l[2].split(".")[-1]
                seq=l[6].split("(")[0]
                
                if l[0]=='20:59:17.744462':
                    print "d"
                
                if tmprec[thr][1]!=seq:
    #                 if int(tmprec[thr][5])==0:
    #                     print "dropser"
                    if tmprec[thr][0]!='0' and int(tmprec[thr][5])!=0 :  #first cond for checking for the first record & second for the requests that has not results
    #                     print l                                 #check weather  it is not the firstrecord
                        tmp=[]                                              #then add thread no,Start time,End time, Duration
                        tmp.append(thr)
                        tmp.append(tmprec[thr][2])
                        tmp.append(tmprec[thr][5])
                        tmp.append(round((tmp[2]-tmp[1]),6))
                        serrecord.append(tmp)
                        tmprec[thr][3]='0'
                        tmprec[thr][4]='0'
                        tmprec[thr][5]='0'
                    tmprec[thr][0]=l[8]                               #add ack no
                    tmprec[thr][1]=seq                                #add seq no
                    tmprec[thr][2]=timeconv(l[0])                     #add send time
                   
    
            elif ".".join(l[4].split(".")[0:clilen])==cliname and l[7]=="ack" and l[4].split(".")[-1][:-1] in tmprec.keys():
                if tmprec[l[4].split(".")[-1][:-1]][0]!='0' and tmprec[l[4].split(".")[-1][:-1]][1].split(":")[1]==l[8]:                          
                    tmprec[l[4].split(".")[-1][:-1]][3]=l[8]                        #add ack no
                    tmprec[l[4].split(".")[-1][:-1]][4]=l[6].split("(")[0]          #add seq no
                    tmprec[l[4].split(".")[-1][:-1]][5]=timeconv(l[0])              #add receieve time
 
    else:
        for line in f:
            l=line.lower().rstrip().split(" ");
            if len(l)==1:
                break
            if len(l)<19:
                continue
            if l[6]=='[s.],' or l[6]=='[s],':
                continue
#             if l[20]=='length' and l[21]=='0':
#                 continue
    
            if ".".join(l[4].split(".")[0:clilen])==cliname and l[4].split('.')[-1][:-1] not in tmprec.keys() and only1thr==False:
                tmprec[l[4].split(".")[-1][:-1]]=['0','0','0','0','0','0']
            if ".".join(l[2].split(".")[0:clilen])==cliname and l[2].split('.')[-1] not in tmprec.keys() and only1thr==False:
                tmprec[l[2].split(".")[-1]]=['0','0','0','0','0','0']

            if int(l[8][:-1].split(":")[0])<10:
                continue
            
            #find the Server side latency 
            if ".".join(l[2].split(".")[0:clilen])==cliname and l[7]=="seq" and l[2].split(".")[-1] in tmprec.keys():
                thr=l[2].split(".")[-1]
                seq=l[8][:-1]
                
                if tmprec[thr][1]!=seq:
                    if tmprec[thr][0]!='0' and int(tmprec[thr][5])!=0 :  #first cond for checking for the first record & second for the requests that has not results
    #                     print l                                 #check weather  it is not the firstrecord
                        tmp=[]                                              #then add thread no,Start time,End time, Duration
                        tmp.append(thr)
                        tmp.append(tmprec[thr][2])
                        tmp.append(tmprec[thr][5])
                        tmp.append(round((tmp[2]-tmp[1]),6))
                        serrecord.append(tmp)
                        tmprec[thr][3]='0'
                        tmprec[thr][4]='0'
                        tmprec[thr][5]='0'
                    tmprec[thr][0]=l[10][:-1]                               #add ack no
                    tmprec[thr][1]=seq                                #add seq no
                    tmprec[thr][2]=timeconv(l[0])                     #add send time

            
            elif ".".join(l[4].split(".")[0:clilen])==cliname and l[7]=="seq" and l[9]=="ack" and l[4].split(".")[-1][:-1] in tmprec.keys():
#                 if l[0]=='13:01:21.681052':
#                     print l
                if tmprec[l[4].split(".")[-1][:-1]][0]!='0' and tmprec[l[4].split(".")[-1][:-1]][1].split(":")[1]==l[10][:-1]:                          
                    tmprec[l[4].split(".")[-1][:-1]][3]=l[10][:-1]                       #add ack no
                    tmprec[l[4].split(".")[-1][:-1]][4]=l[8][:-1]          #add seq no
                    tmprec[l[4].split(".")[-1][:-1]][5]=timeconv(l[0])              #add receieve time

    
    return serrecord,tmprec.keys()

###################################################################################
'''Cassandra Server side Latency in millisecond'''
def serv_side_lat(fipath,finame,serthrs,serrec):
    for i in range(len(serthrs)):
        list4plot=[]
        time4plot=[]
        #print "thrad:",thrs[i]
        for x in serrec:
            if x[0]==serthrs[i]:
                #print "threads:",x
                list4plot.append(x[4]*1000)
                time4plot.append(x[2])
        plot(fipath,finame,list4plot,time4plot,'ser')
    print "serrec",serrec
#########################################################################################    
'''Cassandra Operation Latency in millisecond'''
def cli_cass_lat(fipath,finame,clithrs,clirec):
    for i in range(len(clithrs)):
        list4plot=[]
        time4plot=[]
        #print "thrad:",thrs[i]
        for x in clirec:
            if x[0]==clithrs[i]:
                #print "threads:",x
                list4plot.append(x[4]*1000)
                time4plot.append(x[2])
        plot(fipath,finame,list4plot,time4plot,'cli')
    print "clirec",clirec
#########################################################################################
''' Time series of the packet interval'''
def timeseri_int(clithrs,filepath):
    for i in range(len(clithrs)):
        timeseries(clithrs[i],filepath)
#########################################################################################
'''Cassandra Operation Latency in millisecond'''
def cli_lat_thput(fipath,finame,his,thrs,rec,serfilepath,intvl,pltintvl,mstpltlst):
    for i in range(len(thrs)):
        list4plot=[]
        time4plot=[]
        #print "thrad:",thrs[i]
        for x in rec:
            if x[0]==thrs[i]:
                #print "threads:",x
                list4plot.append(x[4]*1000)
                time4plot.append(x[2])
        #print "dsds",list4plot,time4plot
        plt_serv_lat_thput_1axis(fipath,finame,his,serfilepath, intvl,list4plot,time4plot,pltintvl)
        
#########################################################################################

# filepath='qmul\\gen3qm.txt'
# cliname='planetlab1.nrl.eecs.qmul.ac.uk'
# sername='planetlab02.sys.virginia.edu' 
# clirec,clithrs=thrclient(filepath) 
# serpath='qmul\\gen3vir.txt'
# serrec,serthrs=thrserver(serpath,cliname,sername)
# 
# serv_side_lat(serthrs, serrec)  #Server side latency
# cli_cass_lat(clithrs, clirec)   #Cassandra Client Latency 
# timeseri_int(clithrs, filepath) #Timeseries of the interval




#rec=thrclient('4over/itchclidmp3gen12.txt')
#print "##########################",len(rec) ,rec[0]
# print "client threads:",clithrs
# print "No of Threads:",len(clithrs)
# print "server threads:",serthrs

'''Cassandra Server side Latency per millisecond'''
# for i in range(len(serthrs)):
#     list4plot=[]
#     time4plot=[]
#     #print "thrad:",thrs[i]
#     for x in serrec:
#         if x[0]==serthrs[i]:
#             #print "threads:",x
#             list4plot.append(x[4]*1000)
#             time4plot.append(x[2])
#     plot(list4plot,time4plot,'ser')
# print "serrec",serrec
'''Cassandra Operation Latency per millisecond'''
# for i in range(len(clithrs)):
#     list4plot=[]
#     time4plot=[]
#     #print "thrad:",thrs[i]
#     for x in clirec:
#         if x[0]==clithrs[i]:
#             #print "threads:",x
#             list4plot.append(x[4]*1000)
#             time4plot.append(x[2])
#     plot(list4plot,time4plot,'cli')
# ''' Time series of the packet interval'''
# for i in range(len(clithrs)):
#     timeseries(clithrs[i],filepath)


 