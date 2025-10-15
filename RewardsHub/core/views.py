from django.shortcuts import render
from django.http import HttpRequest, JsonResponse

# Create your views here.
def index(request: HttpRequest):
    return render(request, "core/index.html")

def test_api(request: HttpRequest):
    return JsonResponse({"message": "Hello from RewardsHub!"})