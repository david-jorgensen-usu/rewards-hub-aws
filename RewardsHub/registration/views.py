import json
from django.http import JsonResponse, HttpRequest
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt  # only for testing — remove later when using tokens!
def sign_up(req):
    if req.method == "POST":
        try:
            data = json.loads(req.body.decode("utf-8"))
            email = data.get("email")
            password = data.get("password")
            first_name = data.get("first_name", "")
            last_name = data.get("last_name", "")

            if not email or not password:
                return JsonResponse({"error": "Email and password required."}, status=400)

            if User.objects.filter(username=email).exists():
                return JsonResponse({"error": "User already exists."}, status=400)

            user = User.objects.create_user(
                username=email,
                password=password,
                email=email,
                first_name=first_name,
                last_name=last_name,
            )

            login(req, user)
            return JsonResponse({"message": "User created successfully", "user_id": user.id}, status=201)

        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)

    return JsonResponse({"error": "Only POST requests allowed"}, status=405)


@csrf_exempt
def sign_in(req: HttpRequest):
    pass
