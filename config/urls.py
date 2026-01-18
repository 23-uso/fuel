from django.contrib import admin
from django.urls import path
from fuel import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.fuel_list, name='home'), # トップページも一覧画面にする
    path('fuel/list/', views.fuel_list, name='fuel_list'),
    path('fuel/add/', views.add_fuel_record, name='add_fuel'),
    path('car/add/', views.register_car, name='register_car'),
    # ★追加：削除用のURL
    path('car/delete/<int:car_id>/', views.delete_car, name='delete_car'),
]
