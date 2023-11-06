from django.urls import path
from . import views

app_name = 'discount_tickets'

urlpatterns = [
    path('restaurant/<uuid:restaurant_id>', views.ListTicketsView.as_view(), name='ticket-list'),
    path('restaurant/<uuid:restaurant_id>/ticket/<uuid:ticket_id>', views.RUDTicketView.as_view(), name='ticket-rud'),
    path('restaurant/<uuid:restaurant_id>/create', views.CreateTicketView.as_view(), name='create-ticket'),
]
