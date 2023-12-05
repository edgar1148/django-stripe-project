from django.urls import path

from .views import (
    ItemDetailView,
    ItemListView,
    CreateStripeCheckoutSessionView,
    CancelView,
    SuccessView,
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
]
