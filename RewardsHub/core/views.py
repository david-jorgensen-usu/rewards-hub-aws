from django.shortcuts import render
from django.http import HttpRequest
from django.views.decorators.csrf import csrf_exempt
import json

# Create your views here.
def index(request: HttpRequest):
    return render(request, "core/index.html")

def test_api(request: HttpRequest):
    return JsonResponse({"message": "Hello from RewardsHub!"})

@csrf_exempt  # 👈 for now, to allow POSTs from your Expo app (simplifies dev)
def feedback_api(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            feedback = data.get("feedback")
            print(f"🐱 Rhemi received feedback: {feedback}")
            return JsonResponse({"status": "success", "message": "Thanks for your feedback!"})
        except json.JSONDecodeError:
            return JsonResponse({"status": "error", "message": "Invalid JSON"}, status=400)
    else:
        return JsonResponse({"status": "error", "message": "Only POST allowed"}, status=405)