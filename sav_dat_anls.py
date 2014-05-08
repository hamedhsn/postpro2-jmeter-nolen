import math
import numpy as np
from pylab import *
# from _xmlplus.xpath.CoreFunctions import Position
############################# CSV  ######################################################
'''Cassandra Server side Latency write to a csv file'''
from fileinput import close
def sav_ser_lat(fipath,finame,serthrs,serrec):
    fi=open(fipath[:-3]+finame+'.csv', "w")
    for i in range(len(serthrs)):
        #print "thrad:",thrs[i]
        cnt=1
        for x in serrec:
            if x[0]==serthrs[i]:
                cnt+=1
                strg=str(serthrs[i])+','+str(x[2])+','+str(x[4]*1000)+',0'+'\n'
                print strg
                fi.write(strg)
        fi.write(str(serthrs[i])+','+str(x[2])+','+str(x[4]*1000)+','+str(cnt)+'\n')
#         fi.close()
##############################  CSV  #####################################################
'''writing Traffic at client and server side to a csv file'''
def sav_trf_cns(fipath,finame,h11,h12,h21,h22):
    fi=open(fipath[:-4]+finame+'.csv', "w")
    print 'his:',h11
    print 'his:',h12
    print 'his:',h21
    print 'his:',h22
    for i in range(min(len(h11),len(h12),len(h21),len(h22))):
        strg=str(h11[i])+','+str(h12[i])+','+str(h21[i])+','+str(h22[i])+'\n'
        fi.write(strg)
#     fi.close()
###################################################################################
'''Cassandra Server side Latency write to a list for the boxplot'''
from fileinput import close
def sav_ser_lat_boxplt(fipath,finame,serthrs,serrec,intvl):
    mstpltlst=[]
    tmplst=[]
    intvl=intvl/1000.0
    cnt=intvl 
    serrec.sort(key=lambda x: x[1])
    baset=math.floor((serrec[0][1]))    
    #list.sort(serrec[:][2])    
    for i in range(len(serrec)):
        if serrec[i][1]<baset+cnt:
            tmplst.append([serrec[i][3]*1000])
        else:
            tmplst=np.asarray(tmplst)
            mstpltlst.append(tmplst)
            tmplst=[]
            tmplst.append([serrec[i][3]*1000])
            cnt+=intvl
#     figure()
#     boxplot(mstpltlst,0,'')
#     show()
    return(mstpltlst)
###################################################################################
'''Cassandra Server side Latency write to a list for the boxplot'''
from fileinput import close
def sav_cli_lat_boxplt(fipath,finame,clithrs,clirec,intvl):
    climstpltlst=[]
    tmplst=[]
    intvl=intvl/1000.0
    cnt=intvl 
    clirec.sort(key=lambda x: x[2])
    baset=math.floor((clirec[0][2]))    
    #list.sort(serrec[:][2])    
    for i in range(len(clirec)):
        if clirec[i][2]<baset+cnt:
            tmplst.append([clirec[i][3]*1000])
        else:
            tmplst=np.asarray(tmplst)
            climstpltlst.append(tmplst)
            tmplst=[]
            tmplst.append([clirec[i][3]*1000])
            cnt+=intvl
#     figure()
#     boxplot(mstpltlst,0,'')
#     show()
    return(climstpltlst)
###################################################################################
'''Thraffic created by client and server side'''
def sav_trf_barplt(serthrs,serrec,clithrs,clirec,intvl):
    his11=[]
    his12=[]
    his21=[]
    his22=[]
    tmph11=0
    tmph12=0
    tmph21=0
    tmph22=0
    tmplst=[]
    
    #while(1):
    intvl=intvl/1000.0
    cnt11=intvl 
    cnt12=intvl
    cnt21=intvl
    cnt22=intvl
    base11=math.floor((clirec[0][1]))    
    base21=math.floor((clirec[0][2]))
    base12=math.floor((serrec[0][1]))
    base22=math.floor((serrec[0][2]))    
    #CLient side traffic
    clirec.sort(key=lambda x: x[1])
    for i in range(len(clirec)):
        if clirec[i][1]<base11+cnt11:
            tmph11+=1
        else:
            his11.append(tmph11)
            tmph11=0
            tmph11+=1
            cnt11+=intvl
    #Find his21 
    clirec.sort(key=lambda x: x[2])
    for i in range(len(clirec)):
        if clirec[i][2]<base21+cnt21:
            tmph21+=1
        else:
            his21.append(tmph21)
            tmph21=0
            tmph21+=1
            cnt21+=intvl
    #server Side Traffic        
    serrec.sort(key=lambda x: x[1])
    for i in range(len(serrec)):
        if serrec[i][1]<base12+cnt12:
            tmph12+=1
        else:
            his12.append(tmph12)
            tmph12=0
            tmph12+=1
            cnt12+=intvl
    #Find his22
    serrec.sort(key=lambda x: x[2])
    for i in range(len(serrec)):
        if serrec[i][2]<base22+cnt22:
#             print serrec[i]
            tmph22+=1
        else:
            his22.append(tmph22)
            tmph22=0
            tmph22+=1
            cnt22+=intvl

#     figure()
#     bar(mstpltlst,0,'')
#     show()
    return(his11,his12,his21,his22)
##############################################################################
''' Plot the throughput and latency in the same plot'''
def plt_serv_box_ser_lat(fipath,finame,his,serfilepath,intvl,st,en,grintvl,mstpltlst,ylimst,ylimen):

#     print len(mstpltlst[90]),mstpltlst[90]
    h=np.asarray(his)
    b=[]
    if grintvl==0:
        for i in range(en-st):
            b.append(st+i)
        b=np.asarray(b)
        plt.bar(b,h[st:en],color='y',align='center')
        plt.boxplot(mstpltlst[st:en],positions=b[st:len(mstpltlst[st:en])],sym='') 
        plt.ylim(ylimst,ylimen) 
        plt.grid()
        plt.show()
    else:
        for i in range(en):
            b.append(i+1)
        b=np.asarray(b)
        for i in range((en-st)/grintvl):
            plt.boxplot(mstpltlst[st+(i*grintvl)-1:st+(i+1)*grintvl],positions=b[st+(i*grintvl)-1:st+(i+1)*grintvl],sym='')
            plt.bar(b[st+(i*grintvl)-1:st+(i+1)*grintvl],h[st+(i*grintvl)-1:st+(i+1)*grintvl],color='y',align='center')  
            plt.show()

    
#     figure = plt.gcf() # get current figure
#     figure.set_size_inches(18.5,10.5 )
#     figure.savefig(fipath[:-4]+finame+str(rpt))
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
#     print "bins",bins                  
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
