from django.urls import path
from . import views

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'), 
    path('list/', views.ProductListView.as_view(), name='list'), 
    path('detail/<int:pk>/', views.ProductDetailView.as_view(), name='detail'), 
    path('search/', views.Productsearch, name='search'), 
]