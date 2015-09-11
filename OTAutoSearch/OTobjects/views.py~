from django.shortcuts import render
from django.core.paginator import Paginator
from OTobjects.models import OTuniq as Model1, OTcands as Model2, Catfiles as Model3, Fchart as Model4
import scipy as sp

# Create your views here.
def Index(request,phref,page=None,per_page=30):
    '''phref    : the prefix of url of paginator
       page     : the current page
       per_page : the number of records in pre page
    '''
    #-page
    if page == None:
        page = 1
    else:
        page = int(page)
    if page >= 4:
        page_start = page-2
        page_end = page+7
    else:
        page_start = 1
        page_end = 1
    #-Select from OTuniq
    otm1 = Model1.objects.order_by('-counts')
    #-Paginator
    paginator = Paginator(otm1,per_page)
    otm1 = paginator.page(page)
    dic = {'otm1':otm1,'paginator':paginator,'page':page,'page_start':page_start,'page_end':page_end,'phref':phref}
    return render(request,'OTobjects/index.html',dic)

def ShowImage(request,otid):
    #-Select from Fchart
    otm4 = Model4.objects.filter(OTid=otid)
    dic = {'otm4':otm4,'otid':otid} 
    return render(request,'OTobjects/showImage.html',dic)


def ShowLightCurve(request,otid,JDC=2456000):
    #-Select from OTcands
    otm2 = Model2.objects.filter(OTid=otid)
    jdmag = sp.asarray([[ot.Catid.JD,ot.magorig]for ot in otm2])
    jdmag = jdmag[jdmag[:,0].argsort()]
    jdmag[:,0] = jdmag[:,0]-JDC
    jdmag = jdmag.tolist()
    dic = {'jdmag':jdmag,'jdc':JDC,'otid':otid}
    return render(request,'OTobjects/showLightCurve.html',dic)

def ShowFchart(request,otid):
    #-Select from Fchart
    otm4 = Model4.objects.filter(OTid=otid)
    dic = {'otm4':otm4,'otid':otid}
    return render(request,'OTobjects/showFchart.html',dic)
