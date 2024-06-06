"""
URL configuration for ecommerce project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from Back.views.user_register_view import UserCreate
from Back.views.token_obtain_pair_view import MyTokenObtainPairView
from Back.views.order import CreateOrderView, ListOrdersView, DeleteOrderView

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('Back.urls.product_urls')),  # le chemin vers le fichier de route des produits product_url
    path('', include('Back.urls.user_urls')),  # le chemin vers le fichier de route du user user_urls
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('login/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'), # route pour le login
    path('register/', UserCreate.as_view(), name='user_register'), # route pour le register
    path('create-order/', CreateOrderView.as_view(), name='create-order'),
    path('list-orders/', ListOrdersView.as_view(), name='list-orders'),
    path('create-order/<int:order_id>/', DeleteOrderView.as_view(), name='delete-order'),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)