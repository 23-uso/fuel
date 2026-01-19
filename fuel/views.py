import requests
import random
from django.db.models import Sum
from django.shortcuts import render, redirect, get_object_or_404
from .models import Car, FuelRecord
from django.contrib.auth.models import User
from django.utils import timezone 

BACKGROUND_IMAGES = [
    "https://images.unsplash.com/photo-1502602898657-3e91760cbb34?q=80&w=1920&auto=format&fit=crop",
    "https://images.unsplash.com/photo-1496442226666-8d4a0e62e6e9?q=80&w=1920&auto=format&fit=crop",
    "https://images.unsplash.com/photo-1513635269975-59663e0ac1ad?q=80&w=1920&auto=format&fit=crop",
    "https://images.unsplash.com/photo-1516483638261-f4dbaf036963?q=80&w=1920&auto=format&fit=crop",
]

def get_random_bg():
    return random.choice(BACKGROUND_IMAGES)

def get_or_create_user(request):
    if not request.user.is_authenticated:
        if not User.objects.exists():
            User.objects.create_superuser('admin', 'admin@example.com', 'password')
        request.user = User.objects.first()
    return request.user

def get_weather_text(code):
    weather_map = {
        0: "快晴☀️", 1: "晴れ🌤", 2: "薄曇り⛅️", 3: "曇り☁️",
        45: "霧🌁", 48: "霧🌁", 51: "霧雨🌧", 53: "霧雨🌧", 55: "霧雨🌧",
        61: "雨☔️", 63: "雨☔️", 65: "激しい雨☔️", 71: "雪❄️", 73: "雪❄️", 75: "吹雪❄️",
        80: "にわか雨🌦", 81: "にわか雨🌦", 82: "豪雨⛈", 95: "雷雨⚡️", 96: "雷雨⚡️", 99: "雷雨⚡️"
    }
    return weather_map.get(code, "不明")

def add_fuel_record(request):
    get_or_create_user(request)
    cars = Car.objects.filter(user=request.user)
    bg_image = get_random_bg()
    
    if request.method == 'POST':
        car_id = request.POST.get('car_id')
      
        distance = float(request.POST.get('distance') or 0)
        fuel_amount = float(request.POST.get('fuel_amount') or 0)
        cost = int(request.POST.get('cost') or 0)
        
        if fuel_amount > 0:
            efficiency = distance / fuel_amount
        else:
            efficiency = 0.0
       
        date = request.POST.get('date')
        if not date:
            date = timezone.now().date() 
    
        lat, lon = 36.56, 136.66 
        try:
            api_url = f'https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true'
            response = requests.get(api_url) 
            w_code = response.json()['current_weather']['weathercode']
        except:
            w_code = None
        
        FuelRecord.objects.create(
            car_id=car_id,
            date=date,
            distance=distance,
            fuel_amount=fuel_amount,
            cost=cost,
            efficiency=round(efficiency, 2),
            weather_code=w_code
        )
        return redirect('fuel_list')

    return render(request, 'fuel.html', {'cars': cars, 'bg_image': bg_image})

def register_car(request):
    get_or_create_user(request)
    current_count = Car.objects.filter(user=request.user).count()
    bg_image = get_random_bg()
    if request.method == 'POST':
        if current_count >= 4:
            return render(request, 'car.html', {'error': "4台までです", 'car_count': current_count, 'bg_image': bg_image})
        Car.objects.create(
            user=request.user,
            name=request.POST['name'],
            manufacturer=request.POST.get('manufacturer', ''),
            car_number=current_count + 1
        )
        return redirect('fuel_list')
    return render(request, 'car.html', {'car_count': current_count, 'bg_image': bg_image})

def delete_car(request, car_id):
    get_or_create_user(request)
    car = get_object_or_404(Car, id=car_id, user=request.user)
    if request.method == 'POST':
        car.delete()
        return redirect('fuel_list')
    return redirect('fuel_list')

def fuel_list(request):
    get_or_create_user(request)
    user = request.user
    bg_image = get_random_bg()

    cars = Car.objects.filter(user=user)
    car_stats = []
    for car in cars:
        data = FuelRecord.objects.filter(car=car).aggregate(
            total_dist=Sum('distance'),
            total_fuel=Sum('fuel_amount'),
            total_cost=Sum('cost')
        )
        if data['total_dist'] and data['total_fuel'] and data['total_fuel'] > 0:
            avg = round(data['total_dist'] / data['total_fuel'], 2)
        else:
            avg = None
        
        car_stats.append({
            'name': car.name, 
            'avg': avg, 
            'id': car.id,
            'total_cost': data['total_cost'] or 0
        })

    records = FuelRecord.objects.filter(car__user=user).order_by('-date')
    for record in records:
        record.weather_text = get_weather_text(record.weather_code)
    
    return render(request, 'list.html', {
        'records': records, 
        'bg_image': bg_image,
        'car_stats': car_stats
    })
