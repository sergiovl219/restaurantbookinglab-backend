from django.shortcuts import redirect


def swagger_view(request):
    """
    Redirects to the Swagger UI.

    This view is used to redirect to the Swagger UI, which provides interactive
    documentation for the API endpoints.

    Args:
        request (HttpRequest): The HTTP request.

    Returns:
        HttpResponseRedirect: A redirection response to the Swagger UI.

    """
    return redirect('schema-swagger-ui')
