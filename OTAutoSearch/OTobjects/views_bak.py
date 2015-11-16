from django.shortcuts import render,render_to_response
from django.http import HttpResponseRedirect
from django.core.paginator import Paginator
from OTobjects.models import OTuniq as Model1, OTcands as Model2, Catfiles as Model3, Fchart as Model4, Comments as Model5, Users as Model6
import scipy as sp

global OTid 

# Create your views here.
def Index(request,status=None,page=None,per_page=30):
    '''page     : the current page
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
    #- check the user from the session
    if 'user_id' in request.session:
        user = Model6.objects.get(uid=request.session['user_id'])
        username = user.uname
        userstatus = True
    else:
        username = None
        userstatus = False
    #-Select from OTuniq
    if status:
        otm1 = Model1.objects.filter(status=status).order_by('-counts')
    else:
        otm1 = Model1.objects.order_by('-counts')
    #-Paginator
    paginator = Paginator(otm1,per_page)
    otm1 = paginator.page(page)
    dic = {'otm1':otm1,'paginator':paginator,'page':page,'page_start':page_start,'page_end':page_end,'username':username,'userstatus':userstatus}
    return render(request,'OTobjects/index.html',dic)

def ShowImage(request,otid):
    global OTid
    OTid = str(otid)
    return render_to_response('OTobjects/showImage.html')


def ShowLightCurve(request,otid,JDC=2450000):
    #-Select from OTcands
    otm2 = Model2.objects.filter(OTid=otid)
    jdmag = sp.asarray([[ot.Catid.JD,ot.magorig]for ot in otm2])
    jdmag[:,0] = jdmag[:,0]-JDC
    jdmag = jdmag[jdmag[:,0].argsort()]
    #jdmag = sp.loadtxt('/home/madong/projects/django/OTAutoSearch/OTobjects/OGLE-SMC-LPV-00189.dat',usecols=[0,1])
    jdmag = jdmag.tolist()    
    dic = {'jdmag':jdmag,'jdc':JDC,'otid':otid}
    return render(request,'OTobjects/showLightCurve.html',dic)

def ShowFchart(request,otid):
    #-Select from Fchart
    otm4 = Model4.objects.filter(OTid=otid)
    dic = {'otm4':otm4,'otid':otid}
    return render(request,'OTobjects/showFchart.html',dic)

def Confirm(request,otid):
    #-Check whether the user login
    if 'user_id' in request.session:
        #-Select from Fchart
        otm4_0 = Model4.objects.filter(OTid=otid).first()
        #-Select from Comments
        otm5 = Model5.objects.filter(OTid=otid)
        counts = otm5.count()
        dic = {'otm4_0':otm4_0,'counts':counts,'otm5':otm5}
        return render(request,'OTobjects/confirm.html',dic)
    else:
        return HttpResponseRedirect('/ot/confirm_login-form')

def ChangeStatus(request,otid):
    #-Update OTuniq and Comments
    if request.POST:
        Model1.objects.filter(OTid=otid).update(status=request.POST['status'])
        otm5UidOtidIsExist = Model5.objects.filter(OTid=otid,uid=request.session['user_id'])
        if otm5UidOtidIsExist:
            otm5UidOtidIsExist.update(status=request.POST['status'])
        else:
            Model5.objects.create(OTid_id=otid,uid_id=request.session['user_id'],status=request.POST['status'])
    #-Select from Fchart
    otm4_0 = Model4.objects.filter(OTid=otid).first()
    dic = {'otm4_0':otm4_0}
    return render(request,'OTobjects/changeStatus.html',dic)

def Comment(request,otid):
    #-Insert into Comments
    if request.POST:
        #otm5UidOtidIsExist = Model5.objects.filter(OTid=otid,uid=request.session['user_id'])
        #if otm5UidOtidIsExist:
        #    otm5UidOtidIsExist.update(comment=request.POST['commentarea'])
        #else:
            Model5.objects.create(OTid_id=otid,uid_id=request.session['user_id'],comment=request.POST['commentarea'])
    #-Select from Comments
    otm5 = Model5.objects.filter(OTid=otid)
    counts = otm5.count()
    dic = {'otm5':otm5,'counts':counts}
    return render(request,'OTobjects/listComment.html',dic)

def LoginForm(request,confirm=False):
    if confirm:
        return render(request,'OTobjects/confirm_login.html')
    else:
        return render(request,'OTobjects/login.html')

def Login(request,confirm=False):
    '''user login ang save the user id to the session
    '''
    username = request.POST['uname']
    password = request.POST['passwd']
    if username and password:
        user = Model6.objects.filter(uname=username)
        if user:
            user = user[0]
            if password == user.passwd:
                #if user.status:
                #    return render(request,'OTobjects/login.html',{'message':"The current user has been logined, prohibit login again."})
                #else:
                    #- change the status of user loggin in database
                    user.status = True
                    user.save()
                    #- save the current user to the session
                    request.session['user_id'] = user.uid
                    if confirm:
                        return HttpResponseRedirect('/ot/image/otid=%s/index=confirm/'%OTid)
                    else:
                        return HttpResponseRedirect('/ot/index')
            else:
                return render(request,'OTobjects/login.html',{'message':"Your username and password didn't match."})
        else:
            return render(request,'OTobjects/login.html',{'message':"The user you input dose not exist and you need to signup!"})
    else:
        return render(request,'OTobjects/login.html',{'message':"Please input your user name and password!"})

def Logout(request):
    uid = request.session['user_id']
    #change the status of user
    user = Model6.objects.get(uid=uid)
    user.status = False
    user.save()
    #delete the user from the session
    del request.session['user_id']
    return HttpResponseRedirect('/ot/index')

def SignupForm(request):
    return render(request,'OTobjects/signup_form.html')

def Signup(request):
    uname = request.POST['uname']
    passwd = request.POST['passwd']
    passwdConf = request.POST['passwdConf']
    fname = request.POST['fname']
    lname = request.POST['lname']
    email = request.POST['email']
    memberIsExist = Model6.objects.filter(uname=uname)
    if memberIsExist:
        return render(request,'OTobjects/signup_form.html',{'message':"The user name you input has been used.Please use another."})
    else:
        if uname and passwd and passwdConf and fname and lname and email:
            if passwd == passwdConf:
                Model6.objects.create(uname=uname,passwd=passwd,first_name=fname,last_name=lname,email_add=email)
                return HttpResponseRedirect('/ot/login-form')
            else:
                return render(request,'OTobjects/signup_form.html',{'message':"The tow passwords you inputed do not match."})
        else:
            return render(request,'OTobjects/signup_form.html',{'message':"Please fill in all the signup information(*)."})
