
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
from OTAutoSearch.settings import base_path,static_path
import scipy as sp
import os
from glob import glob
import pyfits
import vaphot as Vap
import GWmatchImage

def intodb(cpath,tempim=None):
   """
   cpath : cat file path
   tempim: template image,Opthion. Default is None
   """
   #-Get the name of cat files
   catna = glob('%s/resi_*.cat'%cpath)
   #-Import data to table
   for c in catna:
       print c
       #-Import data to table (Catfiles)
       resifn = '.'.join((c.rsplit('.',1)[0],'fit'))
       #-Get JD
       try:
           jd = pyfits.getval(resifn,'JD')
       except:
           jd = -999999
       #-Add a record into table (Catfiles)
       if not tempim:
           tempim = 'Temp_%s.fit'%'_'.join(c.rsplit('/',1)[1].split('_')[1:6])
       ref_im = tempim
       ids = c.rsplit('/',1)[1].split('_')
       mountid = ids[1]
       cameraid = ids[2]
       ymd = ids[3]
       skyid = ids[5]
       mcysids = '_'.join([mountid,cameraid,ymd,skyid])
       Catfiles.objects.create(Catna=c.rsplit('/',1)[1],orig_im=c.rsplit('resi_',1)[1],ref_im=tempim,JD=jd,mountid=mountid,cameraid=cameraid,ymd=ymd,skyid=skyid,mcysids=mcysids)
       #-Get catid from table Catfiles
       catid = Catfiles.objects.last().Catid
       #-Read dat data(x,y,mag_aper,magerr_aper)
       datna = '.'.join((c.rsplit('.',1)[0],'dat'))
       try:
           dat = sp.loadtxt(datna,usecols=[1,2,3,4])
       except:
           continue
       # Aimage - Bimage = Cimage
       #-coordinate,original image name ,template image name 
       cor = sp.array(zip(dat[:,0],dat[:,1]))
       #origfn = ''.join(resifn.rsplit('resi_',1))
       rawcomPath = resifn.replace('/difimage/proc','/difimage/rawcom').rsplit('resi_',1)[0]
       origfn = '%s%s'%(rawcomPath,resifn.rsplit('resi_',1)[-1])
       tempfn = '%s%s'%(rawcomPath,tempim)
       #-Calculate original image magorig and magorigErr (Aimage)
       orimag = Vap.DaoAper(origfn,cor,exptime=10,aperture=2.0,gain=1.0,rdnoise=8.0,calgorithm='none',zmag=0)
       #-Calculate template image magref and magrefErr (Bimage)
       tempmag = Vap.DaoAper(tempfn,cor,exptime=10,aperture=2.0,gain=1.0,rdnoise=8.0,calgorithm='none',zmag=0)
       #-parameters for output png    
       imfiles = [origfn,tempfn,resifn]

       #-Import data to table (OTuniq, OTcands)
       if OTuniq.objects.count()>0:
           for i,d in enumerate(dat):
               x_d,y_d = d[:2]
               #init
               dis_min = 1e+15
               id = 0
               x = 0
               y = 0
               #-Output png
               B = GWmatchImage.ImShow(imfiles,d[:2],contrast='zscale', scale='linear', tag_cats=True)
               C = B.plotobj(text=None, oversample=2.0, radius=5.0, color='r', color_b='g', winsize=[100, 100], debug=False)
               outfile = '%s_%i.png'%(c.rsplit('.',1)[0],i)
               C.save(outfile)
               os.system("ln -s  %s %s/OTobjects/Fchart/"%(outfile,static_path))
               #return the value(id,x,y) of cross match
               for o in OTuniq.objects.all():
                   #distance
                   dis = sp.sqrt((x_d-o.x)**2+(y_d-o.y)**2)
                   if dis < dis_min:
                       dis_min = dis
                       id = o.OTid
                       x = o.x
                       y = o.y
               #Write to table or update table
               #Match
               if dis_min <1:
                   print 'update:id=%s x=%s y=%s'%(id,x,y)
                   #-Update table(OTuniq) a record
                   counts = OTuniq.objects.get(OTid=id).counts+1
                   OTcands_sets = OTcands.objects.filter(OTid=id)
                   x_mid = sp.median([o.x for o in OTcands_sets])
                   y_mid = sp.median([o.y for o in OTcands_sets])
                   OTuniq.objects.filter(OTid=id).update(x=x_mid,y=y_mid,magres=d[2],magErr=d[3],magorig=orimag[i,0],magorigErr=orimag[i,1],magref=0,magrefErr=0,counts=counts)
               #No match
               else:
                   #-Add a record into table (OTuniq)
                   OTuniq.objects.create(x=d[0],y=d[1],Ra=d[5],Dec=d[6],magcalib=0,magres=d[2],magErr=d[3],magorig=orimag[i,0],magorigErr=orimag[i,1],magref=0,magrefErr=0,counts=1,c_filter=0)
                   id = OTuniq.objects.last().OTid
                   x = d[0]
                   y = d[1]
                   print 'create:id=%s x=%s y=%s'%(id,x,y)

               #Write to table:OTcands (Whether or not to match)
               OTcands.objects.create(OTid_id=id,Catid_id=catid,x=x,y=y,Ra=d[5],Dec=d[6],magres=d[2],magresErr=d[3],magorig=orimag[i,0],magorigErr=orimag[i,1],magrescalib=0,filter=0,tag_refstr=0)
               #Add records into table:Fchart
               fname = ''.join((c.rsplit('/',1)[1].rsplit('.',1)[0],'_%i.png'%i))
               Fchart.objects.create(OTid_id=id,Catid_id=catid,Fname=fname)

       else:
           for i,d in enumerate(dat):
               #-Add records
               #table:OTuniq
               OTuniq.objects.create(x=d[0],y=d[1],Ra=d[5],Dec=d[6],magcalib=0,magres=d[2],magErr=d[3],magorig=orimag[i,0],magorigErr=orimag[i,1],magref=tempmag[i,0],magrefErr=tempmag[i,1],counts=1,c_filter=0)
#               OTuniq.objects.create(x=d[0],y=d[1],Ra=0,Dec=0,magcalib=0,magres=d[2],magErr=d[3],magorig=0,magorigErr=0,magref=0,magrefErr=0,counts=1,c_filter=0)
               #table:OTcands
               id = OTuniq.objects.last().OTid
               OTcands.objects.create(OTid_id=id,Catid_id=catid,x=d[0],y=d[1],Ra=d[5],Dec=d[6],magres=d[2],magresErr=d[3],magorig=orimag[i,0],magorigErr=orimag[i,1],magrescalib=0,filter=0,tag_refstr=0)
               #-Output png
               B = GWmatchImage.ImShow(imfiles,d[:2],contrast='zscale', scale='linear', tag_cats=True)
               C = B.plotobj(text=None, oversample=2.0, radius=5.0, color='r', color_b='g', winsize=[100, 100], debug=False)
               outfile = '%s_%i.png'%(c.rsplit('.',1)[0],i)
               C.save(outfile)
               os.system("ln -s  %s %s/OTobjects/"%(outfile,static_path))
               #table:Fchart
               fname = ''.join((c.rsplit('/',1)[1].rsplit('.',1)[0],'_%i.png'%i))
               Fchart.objects.create(OTid_id=id,Catid_id=catid,Fname=fname)
