from django.conf.urls import *
from OTobjects import views

phref_dic = {'phref':'/ot/index/'}

urlpatterns = patterns('',
   url(r'index/$',views.Index,phref_dic,name='index'),
   url(r'index/page=(?P<page>\d+)/$',views.Index,phref_dic,name='index_page'),
   url(r'image/otid=(?P<otid>\d+)/$',views.ShowImage,name='image'),
   url(r'image/otid=(?P<otid>\d+)/?index=lc/$',views.ShowLightCurve, name='lc'),
   url(r'image/otid=(?P<otid>\d+)/?index=fchart/$',views.ShowFchart,name='fchart'),
)
