from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets
from rest_framework.decorators import list_route
from rest_framework.permissions import AllowAny

from Auth.models import Company

import smtplib
from_address = 'aybekko97@gmail.com'
username = 'username'
password = 'password'
server = smtplib.SMTP('smtp.gmail.com:587')
server.ehlo()
server.starttls()
server.login(username, password)

class CompanyViewSet(viewsets.ViewSet):
    queryset = Company.objects.all()
    permission_classes = [AllowAny]

    def get_serializer_class(self):
        pass

    # Send code to email and by this code user can register
    @list_route(methods=["POST"], permission_classes=[AllowAny])
    def send_code(self, request):
        #server.sendmail()