from django.urls import path

from .views import (
    CreateStripeCheckoutSessionView,
    CancelView,
    SuccessView,
    orders,
    order_payment,
    stripe_config,
    items_list_view,
    items_detail_view,
    order_detail_view
)

app_name = 'products'


urlpatterns = [
    path('', items_list_view, name='product-list'),
    path('item/<int:pk>/', items_detail_view, name='product-detail'),
    path('buy/<int:pk>/',
         CreateStripeCheckoutSessionView.as_view(),
         name='create-checkout-session',
    ),
    path('success/', SuccessView.as_view(), name='success'),
    path('cancel/', CancelView.as_view(), name='cancel'),
    path('orders/', orders, name='orders'),
    path('orders/<int:pk>/', order_payment, name='order-payment'),
    path('order/<int:pk>/', order_detail_view, name='order-detail'),
    path('config/', stripe_config, name='config'),
]
