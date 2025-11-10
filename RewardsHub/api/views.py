from django.http import HttpRequest, JsonResponse
from django.contrib.auth.decorators import login_required
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.core.mail import send_mail
from rest_framework.response import Response
import json
import logging
from core.models import LinkedApp, AppCatalog, Feedback

logger = logging.getLogger(__name__)

# Create your views here.
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def current_user(request):
    user = request.user

    linked_apps = [
        {
            "reference": la.app.reference,
            "isActive": la.notify,
            "notify": la.notify
        }
        for la in LinkedApp.objects.filter(user=user)
    ]

    data = {
        "id": user.id,
        "username": user.username,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "email": user.email,
        "linked_apps": linked_apps
    }
    return Response(data)

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def link_app(request):
    try:
        user = request.user
        app_name = request.data.get("app_name")  # now clearly a name, not an ID
        notify = request.data.get("notify")

        if not app_name:
            return Response({"error": "Missing app_name"}, status=400)

        # Look up the app by its name
        try:
            app = AppCatalog.objects.get(name=app_name)
        except AppCatalog.DoesNotExist:
            return Response({"error": f"No app found with name '{app_name}'"}, status=404)

        # Get or create the link between user and app
        linked_app, _ = LinkedApp.objects.get_or_create(user=user, app=app)

        # Update the notify field if provided
        if notify is not None:
            linked_app.notify = notify
            linked_app.save()

        return Response({
            "app": app.name,
            "notify": linked_app.notify,
        }, status=200)

    except Exception as e:
        import traceback
        traceback.print_exc()
        return Response({"error": str(e)}, status=500)

@api_view(['GET', 'POST'])
@permission_classes([AllowAny])
def feedback_api(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            feedback_text = data.get("feedback")

            if not feedback_text or not feedback_text.strip():
                return JsonResponse(
                    {"status": "error", "message": "Feedback cannot be empty."},
                    status=400
                )

            user = request.user if request.user.is_authenticated else None

            # Save to database
            feedback_entry = Feedback.objects.create(
                user=user,
                message=feedback_text.strip(),
            )

            logger.info(f"Feedback saved (ID {feedback_entry.id}) from {user or 'Anonymous'}")

            return JsonResponse(
                {"status": "success", "message": "Thanks for your feedback!"}
            )

        except json.JSONDecodeError:
            return JsonResponse(
                {"status": "error", "message": "Invalid JSON"},
                status=400
            )

    elif request.method == "GET":
        return JsonResponse({
            "message": "Send feedback via POST with a 'feedback' field."
        })

    return JsonResponse(
        {"status": "error", "message": "Only GET and POST allowed"},
        status=405
    )

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


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def link_app(request):
    user = request.user
    app_id = request.data.get("app_id")
    notify = request.data.get("notify")  # optional toggle from app

    if not app_id:
        return Response({"error": "Missing app_id"}, status=400)

    try:
        app = AppCatalog.objects.get(id=app_id)
    except AppCatalog.DoesNotExist:
        return Response({"error": "App not found"}, status=404)

    linked_app, created = LinkedApp.objects.get_or_create(user=user, app=app)

    # If a notify value was provided, update it.
    if notify is not None:
        linked_app.notify = bool(notify)
        linked_app.save()
    # Otherwise, leave notify as-is (it defaults to True on creation).

    return Response({
        "success": True,
        "app_id": app_id,
        "notify": linked_app.notify,
        "created": created,
    })


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