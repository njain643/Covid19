from django.urls import path, include
from .views import update_country, update_state_india

urlpatterns =[
    path('dashboard', update_country, name="update_country"),
    path('<slug:name>/', update_state_india, name="update_state_india"),
    # path('update_country', update_country, name="update_country"),
]