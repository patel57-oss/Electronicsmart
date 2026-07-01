from django.urls import path
from . import views

urlpatterns = [
    
    path("", views.home, name="home"),
    path("product/<int:pk>/", views.product_detail, name="product_detail"),
    path("category/<slug:slug>/", views.category_products, name="category_products"),

    path("cart/", views.cart, name="cart"),
    path("add/<int:pk>/", views.add_to_cart, name="add_to_cart"),
    path("remove/<int:pk>/", views.remove_from_cart, name="remove_cart"),

    path("checkout/", views.checkout, name="checkout"),
    path("payment-success/", views.payment_success, name="payment_success"),
    path("product/add/", views.add_product, name="add_product"),

    path("register/", views.register, name="register"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
]