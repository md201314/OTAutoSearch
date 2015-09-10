
#import psycopg2
#import scipy as sp

#-Read data
#dat = sp.loadtxt('/home/madong/work/miniGWAC/test/otpredict/resi_Comb_test_0019_0028_CR3.dat')
#-Connect database
#conn = psycopg2.connect(database='OTdb',user='minigwac',password='gwac',host='localhost',port='5439')
#cur = conn.cursor()
#conn.rollback()
#-Import data to table
#for i,d in enumerate(dat):
#    cur.execute("insert into otuniq values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);",(i,d[1],d[2],0,0,0,d[4],d[3],0,0,0,0))

#------------------
from OTobjects.models import *
import scipy as sp
from glob import glob
import pyfits

#-Get the name of cat files
catna = glob('/home/madong/work/miniGWAC/test/otpredict/resi_Comb_test_*.cat')
#-Import data to table
for c in catna:
    print c
    #-Import data to table (Catfiles)
    fn = '.'.join((c.rsplit('.',1)[0],'fit'))
    #-Get JD
    jd = pyfits.getval(fn,'JD')
    #-Add a record
    Catfiles.objects.create(Catna=c.rsplit('/',1)[1],orig_im='orig_image',ref_im='ref_image',JD=jd)
    #-Get catid from table Catfiles
    catid = Catfiles.objects.last().Catid
    #-Read cat data
    dat = sp.loadtxt(c)
    #-Import data to table (OTuniq, OTcands)
    if OTuniq.objects.count()>0:
        for d in dat:
            x_d = d[1]
            y_d = d[2]
            #init
            dis_min = 1e+15
            id = 0
            x = 0
            y = 0
            #return the value(id,x,y) of cross match
            for o in OTuniq.objects.filter():
                #distance
                dis = sp.sqrt((x_d-o.x)**2+(y_d-o.y)**2)
                if dis < dis_min:
                    dis_min = dis
                    id = o.OTid
                    x = o.x
                    y = o.y
            #Write to table or update table
            #Match
            if dis_min <0.1:
                print 'update:id=%s x=%s y=%s'%(id,x,y)
                #-Update table(Tuniq) a record 
                OTuniq.objects.filter(OTid=id).update(x=x,y=y)
            #No match
            else:
                #-Add a record into table (OTuniq)
                OTuniq.objects.create(x=d[1],y=d[2],Ra=0,Dec=0,magcalib=0,magErr=d[4],magres=d[3],magorig=0,magorigErr=0,counts=0,c_filter=0)
                id = OTuniq.objects.last().OTid
                x = d[1]
                y = d[2]
            #Write to table:OTcands (Whether or not to match)
            OTcands.objects.create(OTid_id=id,Catid_id=catid,x=x,y=y,Ra=0,Dec=0,magres=d[3],magresErr=0,magrescalib=0,filter=0,tag_refstr=0)
    else:
        for d in dat:
            OTuniq.objects.create(x=d[1],y=d[2],Ra=0,Dec=0,magcalib=0,magErr=d[4],magres=d[3],magorig=0,magorigErr=0,counts=0,c_filter=0)
            tmp_id = OTuniq.objects.first().OTid
            OTcands.objects.create(OTid_id=tmp_id,Catid_id=catid,x=d[1],y=d[2],Ra=0,Dec=0,magres=d[3],magresErr=0,magrescalib=0,filter=0,tag_refstr=0)
