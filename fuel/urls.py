from django.urls import path
from . import views

urlpatterns = [
    # 燃費入力画面
    path('fuel/add/', views.add_fuel_record, name='add_fuel'),
    
    # 燃費履歴一覧画面
    path('fuel/list/', views.fuel_list, name='fuel_list'),
    
    # 車の登録画面
    path('car/add/', views.register_car, name='register_car'),
]