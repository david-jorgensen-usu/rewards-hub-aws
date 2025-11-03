from django.shortcuts import render
from django.http import HttpRequest
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import LinkedApp
from django.contrib.auth.models import User

# Create your views here.
def index(request: HttpRequest):
    return render(request, "core/index.html")

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_profile(request):
    user = request.user
    linked_apps = LinkedApp.objects.filter(user=user).select_related('app__category')

    return Response({
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "linked_apps": [
            {
                "id": link.app.id,
                "name": link.app.name,
                "reference": link.app.reference,
                "category": link.app.category.name,
            }
            for link in linked_apps
        ],
    })