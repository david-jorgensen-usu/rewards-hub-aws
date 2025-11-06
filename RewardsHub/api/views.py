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
from core.models import LinkedApp, AppCatalog

# Create your views here.
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def current_user(request):
    user = request.user

    # Build linked apps list as dictionaries
    linked_apps = [
        {
            "reference": la.app.reference,
            "isActive": la.notify,  # map notify to isActive for the frontend
            "notify": la.notify
        }
        for la in LinkedApp.objects.filter(user=user)
    ]

    data = {
        "id": user.id,
        "username": user.username,
        "linked_apps": linked_apps
    }
    return Response(data)

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
        app_ref = request.data.get('app_id')  # your frontend sends 'reference'
        if not app_ref:
            return Response({"error": "Missing app_id"}, status=400)

        try:
            # Lookup by reference (slug-like field)
            app = AppCatalog.objects.get(reference__iexact=app_ref)
        except AppCatalog.DoesNotExist:
            return Response({"error": "App not found"}, status=404)

        linked, created = LinkedApp.objects.get_or_create(user=request.user, app=app)
        if not created:
            return Response({"message": "App already linked"}, status=200)

        return Response({"message": "App linked successfully"}, status=201)

    except Exception as e:
        return Response({"error": str(e)}, status=500)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def unlink_app(request):
    """
    Unlink a LinkedApp for the current user.
    Expects JSON body: {"app_id": "<reference_or_id>"}
    """
    try:
        app_ref = request.data.get('app_id')
        if not app_ref:
            return Response({"error": "Missing app_id"}, status=status.HTTP_400_BAD_REQUEST)

        # Lookup app by reference or numeric ID
        try:
            if str(app_ref).isdigit():
                app = AppCatalog.objects.get(id=int(app_ref))
            else:
                app = AppCatalog.objects.get(reference__iexact=app_ref)
        except AppCatalog.DoesNotExist:
            return Response({"error": "App not found"}, status=status.HTTP_404_NOT_FOUND)

        # Try to delete the link
        try:
            linked = LinkedApp.objects.get(user=request.user, app=app)
            linked.delete()
            return Response({"message": "App unlinked successfully"}, status=status.HTTP_200_OK)
        except LinkedApp.DoesNotExist:
            return Response({"error": "App not linked"}, status=status.HTTP_400_BAD_REQUEST)

    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)