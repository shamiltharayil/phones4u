
# from django import views
from django import urls
from django.contrib import admin
from django.urls import path,include

from phones4u.settings import MEDIA_ROOT
from . import views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/',include('accounts.urls')),
    path('',views.home, name='home'),
    path('store/',include('store.urls')),
    path('cart/',include('carts.urls')),
    path('orders/',include('orders.urls')),
    path('adminapp/',include('adminapp.urls'))
    ] + static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)

 

