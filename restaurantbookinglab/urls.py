from django.contrib import admin
from django.urls import path, re_path, include
from rest_framework.authtoken import views as rest_framework_views
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="Restaurant Booking Lab API",
        default_version='v1',
        description="API documentation for the Restaurant Booking Lab project",
        terms_of_service="https://www.restaurantbookinglab.com/terms/",
        contact=openapi.Contact(email="contact@restaurantbookinglab.com"),
        license=openapi.License(name="MIT License"),
    ),
    public=True,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('restaurant.urls', namespace='restaurant')),
    path('api/tickets/', include('discount_tickets.urls', namespace='discount_tickets')),
    path('api-token-auth', rest_framework_views.obtain_auth_token),
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
]
