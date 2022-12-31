from django.urls import path, include
from . import views
urlpatterns = [

    path('login/', views.MyTokenObtainPairView.as_view(), name='login'),
    path('upload/', views.upload_img, name='upload')
]
