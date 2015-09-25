from django.conf.urls import *
from OTobjects import views

#phref_dic = {'phref':'/ot/index/'}

urlpatterns = patterns('',
   url(r'index$',views.Index,name='index'),
   url(r'status=(?P<status>-?\d{1})/$',views.Index,name='index_status'),
   url(r'status=(?P<status>-?\d)/page=(?P<page>\d+)$',views.Index,name='index_status_page'),
   url(r'page=(?P<page>\d+)$',views.Index,name='index_page'),
   url(r'image/otid=(?P<otid>\d+)/$',views.ShowImage,name='image'),
   url(r'image/otid=(?P<otid>\d+)/?index=lc/$',views.ShowLightCurve, name='lc'),
   url(r'image/otid=(?P<otid>\d+)/?index=fchart/$',views.ShowFchart,name='fchart'),
   url(r'image/otid=(?P<otid>\d+)/?index=confirm/$',views.Confirm,name='confirm'),
   url(r'image/otid=(?P<otid>\d+)/?index=status/$',views.ChangeStatus,name='changestatus'),
   url(r'image/otid=(?P<otid>\d+)/?index=comment/$',views.Comment,name='comment'),
)
