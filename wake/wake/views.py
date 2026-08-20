from django.http import JsonResponse
from django.shortcuts import render

from django.http import JsonResponse
from django.shortcuts import render
from .models import ServerState

from wakeonlan import wake

from variables import TEST_MAC

WAKE_UP = False

def get_or_create_state():
    # Ensure we always have one state row
    state, _ = ServerState.objects.get_or_create(id=1)
    return state

def index(request):
    state = get_or_create_state()
    return render(request, "index.html", {"state": state})

def toggle_button(request):
    url_name = request.resolver_match.url_name

    if request.method == "POST" and url_name == "desktop":
        
        state = get_or_create_state()
        state.button_enabled = not state.button_enabled

        if not state.button_enabled and WAKE_UP:
            wake(TEST_MAC)
            print("Called wake")
        
        state.save()

        return JsonResponse({
            "status": "ok",
            "enabled": state.button_enabled,
            "label": "Enabled" if state.button_enabled else "Disabled"
        })
    
    return JsonResponse({"error": "Invalid request"}, status=400)
