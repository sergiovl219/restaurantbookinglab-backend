import threading

from django.test import TestCase
from rest_framework.test import APIRequestFactory
from rest_framework.test import APIClient
from django.urls import reverse
from rest_framework.authtoken.models import Token
from rest_framework import status
from django.contrib.auth import get_user_model

from discount_tickets.models import Purchase
from discount_tickets.models import Ticket
from restaurant.models import Owner
from restaurant.models import Restaurant

User = get_user_model()


class TicketPurchaseCreateViewTestCase(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.owner = Owner.objects.create(user=self.user)
        self.token, _ = Token.objects.get_or_create(user=self.user)

        self.restaurant = Restaurant.objects.create(name='Test Restaurant', owner=self.owner)
        self.ticket = Ticket.objects.create(
            name='Test Ticket',
            max_purchase=1,
            count=1,
            restaurant=self.restaurant
        )

    def create_purchase(self, quantity: int):
        client = APIClient()

        url = reverse('discount_tickets:ticket-purchase', args=[self.restaurant.id, self.ticket.id])

        data = {
            'quantity': quantity,
        }

        response = client.post(url, data, format='json')
        return response

    def test_successful_purchase(self):
        quantity = 1
        response = self.create_purchase(quantity)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        purchase = Purchase.objects.get()
        self.assertEqual(purchase.ticket, self.ticket)
        self.assertEqual(purchase.guest, None)
        self.assertEqual(purchase.quantity, quantity)

    def test_concurrent_purchases(self):
        num_threads = 2
        threads = []

        def make_purchase():
            self.create_purchase(quantity=1)

        for _ in range(num_threads):
            thread = threading.Thread(target=make_purchase)
            threads.append(thread)
            thread.start()

        for thread in threads:
            thread.join()

        self.assertEqual(Purchase.objects.count(), 1)
