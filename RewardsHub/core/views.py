from django.shortcuts import render
from django.http import HttpRequest, JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

# Create your views here.
def index(request: HttpRequest):
    return render(request, "core/index.html")

def test_api(request: HttpRequest):
    return JsonResponse({"message": "Hello from RewardsHub!"})

@csrf_exempt
def feedback_api(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            feedback = data.get("feedback")
            print(f"🐱 Rhemi received feedback: {feedback}")
            return JsonResponse({"status": "success", "message": "Thanks for your feedback!"})
        except json.JSONDecodeError:
            return JsonResponse({"status": "error", "message": "Invalid JSON"}, status=400)
    
    elif request.method == "GET":
        return JsonResponse({
            "message": "🐱 Rhemi is listening! Send feedback via POST with a 'feedback' field."
        })
    
    else:
        return JsonResponse({"status": "error", "message": "Only GET and POST allowed"}, status=405)