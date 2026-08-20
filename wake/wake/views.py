from django.http import JsonResponse
from django.shortcuts import render

from django.http import JsonResponse
from django.shortcuts import render
from .models import Server

from wakeonlan import wake

from .variables import TEST_MAC

WAKE_UP = False

def get_or_create_state():
    state, _ = Server.objects.get_or_create()
    return state

def index(request):
    servers = list(Server.objects.values("id", "name", "is_on"))

    print(servers)

    return render(request, "index.html", {"servers": servers})

def toggle_button(request):
    url_name = request.resolver_match.url_name

    if request.method == "POST" and url_name == "other":
        server, _ = Server.objects.get_or_create(id=2)
        server.is_on = not server.is_on

        server.save()

        return JsonResponse({
            "status": "ok",
            "enabled": server.is_on,
            "label": "Enabled" if server.is_on else "Disabled"
        })

    if request.method == "POST" and url_name == "desktop":
        
        server, _ = Server.objects.get_or_create(id=1, name="desktop", mac_address=TEST_MAC)
        server.is_on = not server.is_on

        if not server.is_on and WAKE_UP:
            wake(TEST_MAC)
            print("Called wake")
        
        server.save()

        return JsonResponse({
            "status": "ok",
            "enabled": server.is_on,
            "label": "Enabled" if server.is_on else "Disabled"
        })
    
    return JsonResponse({"error": "Invalid request"}, status=400)
