from django.http import HttpRequest, JsonResponse
from django.contrib.auth.decorators import login_required
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework_simplejwt.authentication import JWTAuthentication
import json
import logging
logger = logging.getLogger(__name__)

# Create your views here.
@api_view(["GET"])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def current_user(request):
    if not request.user.is_authenticated:
        return Response({"detail": "Authentication credentials were not provided."}, status=status.HTTP_401_UNAUTHORIZED)

    user = request.user
    return JsonResponse({
        "id": user.id,
        "email": user.email,
        "first_name": user.first_name,
        "last_name": user.last_name,
    })


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def test_api(request: HttpRequest):
    return JsonResponse({"message": "Hello from RewardsHub!"})


@api_view(['GET','POST'])
@permission_classes([AllowAny])
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