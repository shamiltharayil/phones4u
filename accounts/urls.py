from django import views
from django.urls import path
from . import views
 
urlpatterns =[
    path('register/', views.register, name='register'),
    path('login/',views.login,name='login'),
    path('logout/',views.logout,name='logout'),
    
    path('dashboard/',views.dashboard, name='dashboard'),
    # path('',views.dashboard, name='dashboard'),
    path('activate/<uidb64>/<token>/',views.activate,name='activate'),
    path('forgotpassword/',views.forgotpassword, name='forgotpassword'),
    path('resetpassword_validate/<uidb64>/<token>/',views.resetpassword_validate,name='resetpassword_validate'),
    path('resetpassword/',views.resetpassword, name='resetpassword'),
    
    path('edit_profile/',views.edit_profile, name='edit_profile'),
    path('change_password/',views.change_password, name='change_password'),
    path('wishlist/',views.wishlist,name='wishlist'),
    path('add_to_wishlist/<int:id>/',views.add_to_wishlist,name="add_to_wishlist"),
    path('delete_wishlist/<int:id>/',views.delete_wishlist,name="delete_wishlist"),
    path('my_orders/',views.my_orders,name='my_orders'),
]