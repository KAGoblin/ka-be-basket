import requests
from django.conf import settings
from oscarapi.views import basket

K_INVENTORY_BASE_URL = 'http://localhost:8002/api/' \
    if settings.IS_RUN_IN_DEV_ENV \
    else 'https://ka-be-inventory-iuls6xv2yq-uc.a.run.app/api/'
K_OFFER_BASE_URL = 'http://localhost:8004/api/' \
    if settings.IS_RUN_IN_DEV_ENV \
    else 'https://ka-be-offer-iuls6xv2yq-uc.a.run.app/api/'


class BasketView(basket.BasketView):

    def get(self, request, *args, **kwargs):
        # simulate get product details
        requests.get(K_INVENTORY_BASE_URL + 'products')

        # simulate get offer details
        requests.get(K_OFFER_BASE_URL + 'offers')

        return super().get(request, *args, **kwargs)


class LineList(basket.LineList):
    def get(self, request, *args, **kwargs):
        # simulate get product details
        requests.get(K_INVENTORY_BASE_URL + 'products')

        return super().get(request, *args, **kwargs)


class AddProductView(basket.AddProductView):

    def post(self, request, *args, **kwargs):
        # simulate get product details
        requests.get(K_INVENTORY_BASE_URL + 'products')

        return super().post(request, *args, **kwargs)


class AddVoucherView(basket.AddVoucherView):

    def post(self, request, *args, **kwargs):
        # simulate get offer details
        requests.get(K_OFFER_BASE_URL + 'offers')

        return super().post(request, *args, **kwargs)
