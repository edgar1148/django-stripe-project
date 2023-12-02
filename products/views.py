import stripe
from django.conf import settings
from django.shortcuts import redirect
from django.views.generic import TemplateView
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.renderers import TemplateHTMLRenderer
from django.shortcuts import get_object_or_404
from django.http.response import JsonResponse
from rest_framework.views import APIView

from .models import Item
from .serializers import ItemSerializer

stripe.api_key = settings.STRIPE_SECRET_KEY

class ItemListView(generics.ListAPIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'products/product_list.html'
    serializer_class = ItemSerializer

    def get(self, request, *args, **kwargs):
        queryset = Item.objects.all()
        return Response({'products': queryset})

class ItemDetailView(generics.RetrieveAPIView):
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
    Create a checkout session and redirect the user to Stripe's checkout page
    """
    
    def get(self, request, *args, **kwargs):
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
            {"id": checkout_session.id}
        )

    def post(self, request, *args, **kwargs):
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
        return redirect(checkout_session.url)


class SuccessView(TemplateView):
    template_name = 'products/success.html'


class CancelView(TemplateView):
    template_name = 'products/cancel.html'
