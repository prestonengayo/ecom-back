from django.urls import path, include
from rest_framework.routers import DefaultRouter
from Back.views.user_view import UserViewSet

router = DefaultRouter()
router.register(r'users', UserViewSet)
"""
    Ce routeur génère toutes les routes CRUD pour les user
    GET /products/ : Pour récupérer la liste de tous les produits, accessible à tous.
    GET /products/{id}/ : Pour récupérer les détails d'un produit spécifique, accessible à tous.
    POST /products/ : Pour créer un nouveau produit, accessible uniquement aux administrateurs.
    PUT/PATCH /products/{id}/ : Pour mettre à jour un produit existant, accessible uniquement aux administrateurs.
    DELETE /products/{id}/ : Pour supprimer un produit, accessible uniquement aux administrateurs.
"""
urlpatterns = [
    path('', include(router.urls)),
]
