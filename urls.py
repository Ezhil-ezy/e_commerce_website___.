from django.urls import path
from . import views

urlpatterns = [

  path('', views.home, name = 'home'),
  path('register', views.register, name = 'dup_reg'),
  path('login', views.login_, name = 'login'),  
  path('cart', views.cart, name = 'cart'),
  path('confirm', views.confirm, name = 'confirm'),
  path('logout', views.logout_page, name = 'logout'), 
  path('addtocart', views.addtocart, name = 'addtocart'),
  path('changes', views.changes, name = 'changes'),
  path('collections', views.collections, name = 'collections'),
  path('collections/<str:name>', views.collections_view, name = 'collections'),
  path('collections/<str:cat_name>/<pro_name>', views.product_details, name = 'product_details'),
  path('remove/<str:cid>/<int:pqt>', views.remove, name = 'remove'),
  path('remove_f/<str:fid>', views.remove_f, name = 'remove_f'),
  path('fav', views.fav, name = 'fav'),
  path('fav_page', views.fav_page, name = 'fav_page'),


]
