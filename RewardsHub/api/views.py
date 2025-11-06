from django.http import HttpRequest, JsonResponse
from django.contrib.auth.decorators import login_required
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework_simplejwt.authentication import JWTAuthentication
import json
import logging
logger = logging.getLogger(__name__)
from core.models import LinkedApp

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
            "message": "Send feedback via POST with a 'feedback' field."
        })
    
    else:
        return JsonResponse({"status": "error", "message": "Only GET and POST allowed"}, status=405)

@api_view(['GET','POST'])
@permission_classes([IsAuthenticated])
def programs(request):
    # Return LinkedApp objects associated with the authenticated user.
    user = request.user
    if not user or not getattr(user, "is_authenticated", False):
        return JsonResponse({"detail": "Authentication credentials were not provided."}, status=401)

    linked_qs = LinkedApp.objects.filter(user=user).select_related('app')
    results = []
    for linked in linked_qs:
        app = getattr(linked, 'app', None)
        # Try to get a usable URL for the app logo if available
        app_logo = None
        try:
            if app and getattr(app, 'logo', None):
                # app.logo.url may not be available in some environments (e.g., no MEDIA_URL)
                app_logo = request.build_absolute_uri(app.logo.url)
        except Exception:
            app_logo = None

        results.append({
            'id': linked.id,
            'app_id': app.id if app else None,
            'app_name': app.name if app else None,
            'app_logo': app_logo,
            'username': linked.username,
            # intentionally do not return password
        })

    return JsonResponse({'linked_apps': results}, safe=False)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def link_app(request):
    try:
        app_id = request.data.get('app_id')
        if not app_id:
            return Response({"error": "Missing app_id"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            app = AppCatalog.objects.get(id=app_id)
        except AppCatalog.DoesNotExist:
            return Response({"error": "App not found"}, status=status.HTTP_404_NOT_FOUND)

        linked, created = LinkedApp.objects.get_or_create(user=request.user, app=app)
        if not created:
            return Response({"message": "App already linked"}, status=status.HTTP_200_OK)

        return Response({"message": "App linked successfully"}, status=status.HTTP_201_CREATED)

    except Exception as e:
        # Catch all unexpected errors
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)