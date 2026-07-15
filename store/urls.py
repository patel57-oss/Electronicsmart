from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("categories/", views.browse_categories, name="browse_categories"),
    path("product/<int:pk>/", views.product_detail, name="product_detail"),
    path("product/<int:pk>/feedback/", views.submit_feedback, name="submit_feedback"),
    path("category/<slug:slug>/", views.category_products, name="category_products"),
    path("subcategory/<slug:slug>/", views.subcategory_products, name="subcategory_products"),
    path("cart/", views.cart, name="cart"),
    path("add/<int:pk>/", views.add_to_cart, name="add_to_cart"),
    path("remove/<int:pk>/", views.remove_from_cart, name="remove_cart"),
    path("checkout/", views.checkout, name="checkout"),
    path("payment-success/", views.payment_success, name="payment_success"),
    path("search/", views.search_products, name="search"),
    path("product/add/", views.add_product, name="add_product"),
    path("orders/", views.orders, name="orders"),
    path("orders/<int:order_id>/items/", views.order_items, name="order_items"),
    path("orders/<int:order_id>/reorder/", views.reorder, name="reorder"),
    path("orders/<int:order_id>/invoice/", views.download_invoice, name="download_invoice"),
    path("register/", views.register, name="register"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("feedback/", views.contact_feedback, name="contact_feedback"),
    path("profile/", views.profile, name="profile"),
    path('search/', views.search_products, name='search_products'),

]