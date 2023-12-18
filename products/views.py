import stripe
from decimal import Decimal

from django.conf import settings
from django.shortcuts import redirect, get_object_or_404, render
from django.views.generic import TemplateView
from django.http.response import JsonResponse
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.renderers import TemplateHTMLRenderer
from django.urls import reverse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt

from .models import Item, Order, OrderItem
from .serializers import ItemSerializer

stripe.api_key = settings.STRIPE_SECRET_KEY


@csrf_exempt
def stripe_config(request):
    if request.method == 'GET':
        stripe_config = {'publicKey': settings.STRIPE_PUBLISHABLE_KEY}
        return JsonResponse(stripe_config, safe=False)


class ItemListView(generics.ListAPIView):
    """Список продуктов"""
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'products/product_list.html'
    serializer_class = ItemSerializer

    def get(self, request, *args, **kwargs):
        queryset = Item.objects.all()
        return Response({'products': queryset})

class ItemDetailView(generics.RetrieveAPIView):
    """Подробная информация о продукте"""
    template_name = 'products/product_detail.html'
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    renderer_classes = [TemplateHTMLRenderer]

    def get(self, request, pk):
        product = get_object_or_404(Item, pk=pk)
        serializer = ItemSerializer(product)
        return Response({'serializer': serializer, 'product': product})


class CreateStripeCheckoutSessionView(APIView):
    """
    Создание checkout сессии.
    """

    def get(self, request, *args, **kwargs):
        "GET запрос для создания сессии"
        price = Item.objects.get(id=self.kwargs["pk"])
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=[
                {
                    "price_data": {
                        "currency": "usd",
                        "unit_amount": int(price.price) * 100,
                        "product_data": {
                            "name": price.name,
                            "description": price.description,
                        },
                    },
                    "quantity": 1,
                }
            ],
            metadata={"product_id": price.id},
            mode="payment",
            success_url=settings.PAYMENT_SUCCESS_URL,
            cancel_url=settings.PAYMENT_CANCEL_URL,
        )
        return JsonResponse(
            {'sessionId': checkout_session.id}
        )



class SuccessView(TemplateView):
    """Страница успешного платежа."""
    template_name = 'products/success.html'


class CancelView(TemplateView):
    """Страница отмены платежа.
    Пока не реализована проверка статуса платежа."""
    template_name = 'products/cancel.html'




def orders(request):
    """Список заказов"""
    orders = Order.objects.all()
    return render(request, 'products/orders.html', {'orders': orders})

@api_view(['GET', 'POST'])
def order_payment(request, pk):
    """Оплата заказа"""
    order = Order.objects.get(id=pk)
    total_price = order.get_total_price()

    checkout_session = stripe.checkout.Session.create(
        payment_method_types=["card"],
        line_items=[
            {
                "price_data": {
                    "currency": "usd",
                    "unit_amount": int(total_price * Decimal(100)),
                    "product_data": {
                        "name": order.id,
                    },
                },
                "quantity": 1,
            }
        ],
        metadata={"product_id": order.id},
        mode="payment",
        success_url=settings.PAYMENT_SUCCESS_URL,
        cancel_url=settings.PAYMENT_CANCEL_URL,
        )
    return JsonResponse({'sessionId': checkout_session.id})
    
    #return redirect(checkout_session.url)
        
    
    
    

 
 


