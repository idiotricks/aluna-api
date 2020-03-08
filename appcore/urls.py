from django.contrib import admin
from django.urls import path
from rest_framework.routers import DefaultRouter

from auths.views import CustomAuthToken
from products.views import ProductViewSet
from stocks.views import StockCardViewSet, StockInViewSet, ItemInViewSet, StockOutViewSet, ItemOutViewSet
from users.views import UserViewSet, CustomerViewSet, SupplierViewSet

router = DefaultRouter()

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/login/', CustomAuthToken.as_view(), name='customauthtoken')
]

router.register(r'users', UserViewSet, basename='user')
router.register(r'customers', CustomerViewSet, basename='customer')
router.register(r'suppliers', SupplierViewSet, basename='supplier')
router.register(r'products', ProductViewSet, basename='product')
router.register(r'stock-cards', StockCardViewSet, basename='stock-card')
router.register(r'stock-in', StockInViewSet, basename='stock-in')
router.register(r'item-in', ItemInViewSet, basename='item-in')
router.register(r'stock-out', StockOutViewSet, basename='stock-out')
router.register(r'item-out', ItemOutViewSet, basename='item-out')
urlpatterns += router.urls
