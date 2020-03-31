from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('products/', views.products, name='products'),

    path('customer/<str:pk>/', views.customer, name='customer'),
    path('update_customer/<str:pk>/', views.updateCustomer, name='update_customer'),

    path('create_order/<str:pk>/', views.createOrder, name='create_order'),
    path('update_order/<str:pk>/', views.updateOrder, name='update_order'),
    path('delete_order/<str:pk>/', views.deleteOrder, name='delete_order'),

    path('signup/', views.signUp, name='signup'),
    path('signin/', views.signIn, name='signin'),
    path('signout/', views.signOut, name='signout'),

    path('user/', views.userPage, name='user-page'),
    path('account/', views.accountSettings, name='account')
]
