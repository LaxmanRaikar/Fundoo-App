from django.conf.urls import url
from . import views
from django.urls import path
import fundoo.s3_transfer
app_name = 'fundoo'

urlpatterns = [
        url(r'^$', views.user_login, name='login'),
        url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        views.activate, name='activate'),
        url(r'^acc_active_sent/$', views.account_activation_sent, name='acc_active_sent'),
        path('api/login', views.RestLogin.as_view(), name="RestLogin"),
        # path('api/register', views.RegisterRapi.as_view(), name="RegisterApi"),
        url(r'^upload/$',fundoo.s3_transfer.uploadto_aws , name='upload'),
        url(r'^api/register/$' ,views.RegisterRapi.as_view(), name="registerapi"),

        path('index', views.index, name="index"),
        path('dash_board', views.dash_board, name="dashboard"),
        path('login', views.user_login, name='login'),
        path('create', views.createnote, name='createnote'),
        path('delete/<int:pk>', views.delete, name='delete'),
        path('get', views.getnotes, name='get'),
       #  path('get/<int:pk>', views.getnotes, name='getnotes'),
       # path('delete/<int:pk>', views.delete, name="deletenotes"),
       path('update/<int:pk>', views.update, name='update'),
        path('pinned/<int:pk>', views.pinned, name='pinned'),
        path('trash/<int:pk>', views.trash, name='trash'),
        path('trashmenu', views.trashitem, name='trashmenu'),
        path('restoretrash/<int:pk>', views.restore_trash, name='restoretrash'),
        path('is_archive/<int:pk>', views.is_archive, name='is_archive'),
        path('setcolor/<int:pk>', views.setcolor, name='setcolor'),
        path('archi', views.show_archive, name='myarchive'),
        path('copynote/<int:pk>', views.copy_note, name='copynote'),




]



