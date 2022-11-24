from django.urls import path
from . import views


urlpatterns = [
path("adminlogin", views.adminlogin, name="adminlogin"),
path("admin_change_password", views.admin_change_password, name="admin_change_password"),
path("signout", views.signout, name="signout"),
path("admin_dashboard", views.admin_dashboard, name="admin_dashboard"),
path("productlist", views.productlist, name="productlist"),
path("addproduct", views.addproduct, name="addproduct"),
path("addproductgallery", views.addproductgallery, name="addproductgallery"),
path("editproduct/<product_id>", views.editProduct, name="editproduct"),
path("variationlist", views.variationlist, name="variationlist"),
path("addvariation",views.addvariation,name='addvariation'),
path("editvariation/<variation_id>", views.editvariation, name="editvariation"),
path("deletevariation/<variation_id>",views.deletevariation,name="deletevariation"),
path("categorylist/", views.categorylist, name="categorylist"),
path("addcategory", views.addcategory, name="addcategory"),
path("editcategory/<category_id>", views.editcategory, name="editcategory"),
path("deletecategory/<category_id>",views.deletecategory,name="deletecategory"),
path("activeorders", views.activeorders, name="activeorders"),
path("admin_order_detail/<order_id>/", views.admin_order_detail, name="admin_order_detail"),
path("order_history", views.order_history, name="order_history"),
path("order_status_change/",views.order_status_change,name="order_status_change"),
path("activeusers", views.activeusers, name="activeusers"),
path("blockuser/<user_id>", views.blockuser, name="blockuser"),
path("unblockuser/<user_id>", views.unblockuser, name="unblockuser"),
path("deleteuser/<user_id>", views.deleteuser, name="deleteuser"),
path("product_report", views.product_report, name="product_report"),
path("sales_report", views.sales_report, name="sales_report"),
path("couponlist", views.couponlist, name="couponlist"),
path("add_coupon", views.add_coupon, name="add_coupon"),
path("editcoupon/<coupon_id>", views.editcoupon, name="editcoupon"),
path("deletecoupon/<coupon_id>", views.deletecoupon, name="deletecoupon"),
]
 
