from django.urls import path

from .views import (
    ItemDetailView,
    ItemListView,
    CreateStripeCheckoutSessionView,
    CancelView,
    SuccessView,
    orders,
    order_payment,
    stripe_config
)

app_name = 'products'


urlpatterns = [
    path('', ItemListView.as_view(), name='product-list'),
    path('item/<int:pk>/', ItemDetailView.as_view(), name='product-detail'),
    path(
        'buy/<int:pk>/',
        CreateStripeCheckoutSessionView.as_view(),
        name='create-checkout-session',
    ),
    path('success/', SuccessView.as_view(), name='success'),
    path('cancel/', CancelView.as_view(), name='cancel'),
    path('orders/', orders, name='orders'),
    path('orders/<int:pk>/', order_payment, name='order-payment'),
    path('config/', stripe_config, name='config'),
]
