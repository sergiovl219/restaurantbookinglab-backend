from django.shortcuts import redirect


def swagger_view(request):
    return redirect('schema-swagger-ui')
