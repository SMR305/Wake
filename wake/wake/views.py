from django.http import JsonResponse
from django.shortcuts import render

from django.http import JsonResponse
from django.shortcuts import render

from .models import Server
from .variables import TEST_MAC

from wakeonlan import wake

WAKE_UP = False

# Sets up the initial index page and gives it the necessary server information
def index(request):
    servers = list(Server.objects.values("id", "name", "is_on"))

    print(servers)

    return render(request, "index.html", {"servers": servers})

# Test Version of the shared helper in order to test and get a feel for the structure of writing and reading from the database
def toggle_button(request):
    url_name = request.resolver_match.url_name

    # Responds to the 2nd button
    if request.method == "POST" and url_name == "other":
        server, _ = Server.objects.get_or_create(id=2, name="tmp")
        server.is_on = not server.is_on

        server.save()

        return JsonResponse({
            "status": "ok",
            "enabled": server.is_on,
            "label": "Enabled" if server.is_on else "Disabled"
        })

    # Responds to the 1st button
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

    # If the others fail then return an error for an invalid request
    return JsonResponse({"error": "Invalid request"}, status=400)


# 
# Need to handle knowing information about the server to be interacted with via the body of the POST request
# 

# Shared helper function for adding a new server
def add(request):
    name = request.build_absolute_uri().split('/')[4]
    print(name)
    return render(request, "tmp.html")

# Shared helper function for shutting down or starting up a given server
def power(request):
    name = request.build_absolute_uri().split('/')[4]
    print(name)
    return render(request, "tmp.html")

# Shared helper function for requesting a reboot from a given server
def reboot(request):
    name = request.build_absolute_uri().split('/')[4]
    print(name)
    return render(request, "tmp.html")

# Shared helper function for deleting a server from the database
def delete(request):
    name = request.build_absolute_uri().split('/')[4]
    print(name)
    return render(request, "tmp.html")
