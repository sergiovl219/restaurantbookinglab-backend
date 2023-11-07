import threading
import time

from celery.contrib.testing.worker import start_worker
from django.test import TestCase
from rest_framework.test import APIRequestFactory
from rest_framework.test import APIClient
from django.urls import reverse
from rest_framework.authtoken.models import Token
from rest_framework import status
from django.contrib.auth import get_user_model

from discount_tickets import tasks
from discount_tickets.models import Purchase
from discount_tickets.models import Ticket
from restaurant.models import Owner
from restaurant.models import Restaurant
from restaurantbookinglab.celery import app

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

    def test_successful_purchase_queued(self):
        """
        Test a successful purchase queued in Celery.
        Verifies that a purchase is successfully created.
        """
        quantity = 1
        response = self.create_purchase(quantity)
        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)
        self.assertIsNotNone(response.data.get("task_id"))
