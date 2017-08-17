import smtplib
import random

from django.shortcuts import render
from django.core.cache import cache

from rest_framework import viewsets
from rest_framework.decorators import list_route
from rest_framework.permissions import AllowAny, SAFE_METHODS
from rest_framework.response import Response
from rest_framework import status

from channels import Channel

from Auth.models import Company
from Auth.serializers import CompanySerializer

# Create your views here.

# Start email server
from_address = 'aybekko97@gmail.com'
username = 'aybekko97'
password = '391040qQq'
server = smtplib.SMTP('smtp.gmail.com:587')
server.ehlo()
server.starttls()
server.login(username, password)

class CompanyViewSet(viewsets.ViewSet):
    queryset = Company.objects.all()
    permission_classes = [AllowAny]

    def get_serializer_class(self, *args, **kwargs):
        if self.request.method in SAFE_METHODS:
            return CompanySerializer

    # Generate and send code to email, then by this code company's request will be registered
    # required : 'email'
    @list_route(methods=["POST"], permission_classes=[AllowAny])
    def generate_code(self, request):
        email = request.data['email']
        if Company.objects.filter(email = email).count() > 0:
            return Response(status=status.HTTP_302_FOUND, data={'message' : "Company with email '%s' is already registered." % email})
        code = str(random.randint(10000,99999))
        ttl = cache.ttl(email + "_")
        if ttl > 0:
                return Response(status=status.HTTP_302_FOUND, data={'message' : 'You can generate code again after %s seconds.' % ttl})
        try:
            server.sendmail(from_address, email, code)
        except:
            server.login(username, password)
            server.sendmail(from_address, email, code)
        cache.set(email, code, timeout=3600*5)
        cache.set(email + "_", code, timeout=30)
        return Response(status=status.HTTP_200_OK, data={'message' : 'Code is generated. %s' % code})


    # Check for code sent by company
    @list_route(methods=["POST"], permission_classes=[AllowAny])
    def check_code(self, request):
        cache_code = cache.get(request.data['email'])
        if cache_code == request.data['code']:
            serializer = CompanySerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(status=status.HTTP_200_OK, data = {'message' : 'Good job, your request is sent to admin.'})
        if cache_code is None:
            return Response(status=status.HTTP_404_NOT_FOUND, data = {'message' : "There is no code for email '%s'" % request.data['email']})
        return Response(status=status.HTTP_403_FORBIDDEN, data = {'message' : 'Wrong code.'})
