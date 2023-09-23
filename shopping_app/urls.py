from django.urls import path
from . import views
app_name='shopping_app'
urlpatterns = [
          path('',views.allproduct,name='allproduct'),
          path('<slug:c_slug>/',views.allproduct,name='product_by_category'),
          path('<slug:c_slug>/<slug:product_slug>/', views.details, name='pro_detail'),

    ]