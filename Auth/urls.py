from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter
from Auth.views import CompanyViewSet

router = DefaultRouter()

router.register(r'company', CompanyViewSet, base_name='companies')
urlpatterns = [
    url(r'^', include(router.urls))
]
