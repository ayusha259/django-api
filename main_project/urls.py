from django.urls import path, include
from rest_framework.decorators import api_view
from django.shortcuts import redirect
from django.views.generic import TemplateView
from django.conf import settings
from django.conf.urls.static import static

@api_view(['GET'])
def redirect_page(request):
    return redirect('/api')

urlpatterns = [
    path('', redirect_page),
    path('api/', include('api.urls')),
    path('docs/', TemplateView.as_view(
        template_name='swagger.html',
        extra_context={'schema_url':'openapi-schema'}
    ), name='swagger-ui'),
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
