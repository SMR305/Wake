import json
import re

from django.db import IntegrityError
from django.http import JsonResponse
from django.shortcuts import render

from .models import Server
from .variables import TEST_MAC

from wakeonlan import wake

WAKE_UP = False
TEST = True

NAME_RE = r"^[a-zA-Z0-9_-]+$"
MAC_RE = r"^[a-fA-F0-9]{2}(:[a-fA-F0-9]{2}){5}$"
IPv4_RE = r"^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$"
IPv6_RE = r"^(([0-9a-fA-F]{1,4}:){7}[0-9a-fA-F]{1,4}|([0-9a-fA-F]{1,4}:){1,7}:|([0-9a-fA-F]{1,4}:){1,6}:[0-9a-fA-F]{1,4}|([0-9a-fA-F]{1,4}:){1,5}(:[0-9a-fA-F]{1,4}){1,2}|([0-9a-fA-F]{1,4}:){1,4}(:[0-9a-fA-F]{1,4}){1,3}|([0-9a-fA-F]{1,4}:){1,3}(:[0-9a-fA-F]{1,4}){1,4}|([0-9a-fA-F]{1,4}:){1,2}(:[0-9a-fA-F]{1,4}){1,5}|[0-9a-fA-F]{1,4}:((:[0-9a-fA-F]{1,4}){1,6})|:((:[0-9a-fA-F]{1,4}){1,7}|:))$"

# Sets up the initial index page and gives it the necessary server information
def index(request):
    # Just so I can see things about the servers
    servers = list(Server.objects.values())
    print(servers)

    # Actually important code for the home page
    servers = list(Server.objects.values("name", "is_on"))
    return render(request, "index.html", {"servers": servers})

# Obsolete Test Function
def toggle_button(request):
    url_name = request.resolver_match.url_name

    if request.method == "POST" and url_name == "other":
        server, _ = Server.objects.get_or_create(id=2, name="tmp")
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


# 
# Need to handle knowing information about the server to be interacted with via the body of the POST request
# 

# Shared helper function for adding a new server
def add(request):
    if request.method == "POST":
        
        try:
            data = json.loads(request.body or "{}")
        except (json.JSONDecodeError, UnicodeDecodeError):
            data = request.POST

        name = data.get("name")
        ip = data.get("ip_address")
        mac = data.get("mac_address")

        if name is None or ip is None or mac is None:
            return JsonResponse({"error": "Missing necessary field(s)"}, status=400)

        if not TEST:
            if (
                not isinstance(ip, str)
                or not isinstance(mac, str)
                or not isinstance(name, str)
                or not (
                    re.fullmatch(IPv4_RE, ip)
                    or re.fullmatch(IPv6_RE, ip)
                )
                or not re.fullmatch(NAME_RE, name)
                or not re.fullmatch(MAC_RE, mac)
            ):
                return JsonResponse({"error": "One or more fields are improperly structured"}, status=400)

        try:
            server = Server.objects.create(name=name, is_on=False, mac_address=mac, ip_address=ip)
        except IntegrityError:
            return JsonResponse({"error": "Conflicting information with another server"}, status=400)

        return JsonResponse({
            "status": "ok",
            "name": server.name,
            "is_on": server.is_on,
        })

    return JsonResponse({"error": "Invalid request"}, status=400)

# Shared helper function for shutting down or starting up a given server
def power(request):
    if request.method == "POST":

        try:
            data = json.loads(request.body or "{}")
        except (json.JSONDecodeError, UnicodeDecodeError):
            data = request.POST

        name = data.get("name")

        try:
            server = Server.objects.get(name=name)
        except Server.DoesNotExist:
            return JsonResponse({"error": "Server not found"}, status=400)

        server.is_on = not server.is_on

        if not server.is_on and WAKE_UP:
            wake(TEST_MAC)
            print("Called wake")
        
        server.save()

        return JsonResponse({
            "status": "ok",
            "enabled": server.is_on,
        })

    return JsonResponse({"error": "Invalid request"}, status=400)

# Shared helper function for requesting a reboot from a given server
def reboot(request):
    return render(request, "tmp.html")

# Shared helper function for deleting a server from the database
def delete(request):
    return render(request, "tmp.html")
