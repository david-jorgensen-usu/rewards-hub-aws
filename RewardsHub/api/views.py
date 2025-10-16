from django.http import HttpRequest, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
import json
import logging
logger = logging.getLogger(__name__)

# Create your views here.
def test_api(request: HttpRequest):
    return JsonResponse({"message": "Hello from RewardsHub!"})


@csrf_exempt
def feedback_api(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            feedback = data.get("feedback")
            logger.info(f"Feedback received: {feedback}")
            return JsonResponse({"status": "success", "message": "Thanks for your feedback!"})
        except json.JSONDecodeError:
            return JsonResponse({"status": "error", "message": "Invalid JSON"}, status=400)
    
    elif request.method == "GET":
        return JsonResponse({
            "message": "🐱 Rhemi is listening! Send feedback via POST with a 'feedback' field."
        })
    
    else:
        return JsonResponse({"status": "error", "message": "Only GET and POST allowed"}, status=405)