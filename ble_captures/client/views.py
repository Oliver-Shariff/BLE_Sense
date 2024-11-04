from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from client.models import *
from django.views import View
from dataclasses import dataclass, asdict
from dataclasses import dataclass, asdict
from django.http import JsonResponse
from django.core.validators import EmailValidator
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import authenticate, login, logout
from django.core.exceptions import ValidationError
from django.contrib import messages
from django.contrib.auth.models import User
from django.core.serializers import serialize
from django.db.models import Max
import json



def fetch_devices(request):
     # First, get each device's latest packet by timestamp
    latest_packets = (
        Packet.objects
        .values("device_id")
        .annotate(latest_timestamp=Max("time_stamp"))
    )

    # Get the details of each device along with its latest packet and related scanner and group
    devices_with_latest_packet = []
    for entry in latest_packets:
        device_id = entry["device_id"]
        latest_timestamp = entry["latest_timestamp"]
        
        # Get the device, latest packet, and associated scan
        device = Device.objects.get(id=device_id)
        latest_packet = Packet.objects.filter(device=device, time_stamp=latest_timestamp).first()
        
        # Get the latest scan for this packet if it exists
        scan = Scans.objects.filter(packet=latest_packet).select_related("scanner__group").first()
        
        # Print data to confirm values
        print(f"Device ID: {device_id}, Latest Packet: {latest_packet}, Scan: {scan}")
        if scan:
            print(f"Scanner: {scan.scanner}, Group: {scan.scanner.group}")



        # Collect relevant information
        device_data = {
            "id": device.id,
            "oui": latest_packet.oui,
            "company_id": latest_packet.company_id,
            "time_stamp": latest_packet.time_stamp,
            "scanner name": scan.scanner.name if scan else None,
            "group": scan.scanner.group.name if scan else None,
        }

        devices_with_latest_packet.append(device_data)

    return JsonResponse(devices_with_latest_packet, safe=False)

def fetch_pkt_data(request, device_pk):
    # Get packet data for the device
    packet_data = Packet.objects.filter(device=device_pk)
    
    # Serialize packet data and ensure `pk` is included as a field in each packet
    packet_list = [
        {
            "pk": packet["pk"],  # Ensure `pk` is directly included
            **packet["fields"]    # Unpack fields to include other packet data
        }
        for packet in json.loads(serialize('json', packet_data))
    ]
    
    # Get device data
    device_data = Device.objects.get(pk=device_pk)
    device_dict = {
        "id": device_data.id,
    }
    
    # Construct response data
    data = {"packets": packet_list, "this_device": device_dict}
    
    return JsonResponse(data, safe=False)

def devices(request: HttpRequest) -> HttpResponse:
    return render(request, "devices.html")


def fetch_data(request):
    group_data = Group.objects.all().values()
    scanner_data = Scanner.objects.all().values()
    packet_data = Packet.objects.all().values()
    

    group_list = list(group_data)
    scanner_list = list(scanner_data)
    packet_list = list(packet_data)

    data = {"groups": group_list, "scanner": scanner_list, "packets": packet_list}

    return JsonResponse(data, safe=False)


def fetch_pkt_count(request):
    pkt_count = Packet.objects.all().count()

    data = {"pkt_count": pkt_count}

    return JsonResponse(data, safe=False)


def attacks(request: HttpRequest) -> HttpResponse:
    return render(request, "attacks.html")


def company_settings(request: HttpRequest) -> HttpResponse:
    return render(request, "companySettings.html")


def profile(request: HttpRequest) -> HttpResponse:
    return render(request, "profile.html")


def groups(request: HttpRequest) -> HttpResponse:
    context = {"groups": Group.objects.all()}

    return render(request, "groups.html", context=context)


def add_group(request: HttpRequest) -> HttpResponse:
    return render(request, "addGroup.html")


def activity(request: HttpRequest, group_pk) -> HttpResponse:
    context = {
        "this_group": Group.objects.get(pk=group_pk),
        "scanners": Scanner.objects.filter(group=group_pk),
    }

    return render(request, "activity.html", context=context)


def packets(request: HttpRequest, device_pk) -> HttpResponse:
    context = {
        "this_device": Device.objects.get(pk=device_pk),
    }

    return render(request, "packets.html", context=context)


class AddSensor(View):
    def get(self, request: HttpRequest):
        context = {"groups": Group.objects.all()}
        return render(request, "addSensor.html", context=context)

    def post(self, request: HttpRequest):
        form = request.POST
        name = form["name"]
        group_pk = form["group_pk"]
        group = Group.objects.get(pk=group_pk)
        company = None
        raise NotImplemented
        # new_sensor = Scanner(name=name, group=group, company)
        # new_sensor.save()
        # return HttpResponse("Add the scanner")


def dashboard(request: HttpRequest) -> HttpResponse:
    context = {
        "groups": Group.objects.all(),
        "sensors": Scanner.objects.all(),
        "attacks": attacks,
    }

    return render(request, "dashboard.html", context=context)




class Register(View):
    def get(self, request: HttpRequest):
        return render(request, "register.html")

    def post(self, request: HttpRequest):
        form = request.POST
        password1 = form["password1"]
        password2 = form["password2"]
        try:
            validate_password(password1)
        except ValidationError as err:
            messages.error(request, "\n".join(err.messages))
            return render(request, "register.html")

        if not (password1 == password2):
            messages.error(request, ("Passwords do not match. Please try again."))
            return render(request, "register.html")
        email = form["email"]
        try:
            validator = EmailValidator()
            validator(email)
        except ValidationError:
            messages.error(request, ("Not a valid email. Please try again."))
            return render(request, "register.html")
        if User.objects.filter(username=email).first():
            messages.error(request, ("You are already registered. Please log in."))
            return redirect("login")
        _ = User.objects.create_user(username=email, email=email, password=password1)
        user_sign_in = authenticate(request, username=email, password=password1)
        login(request, user_sign_in)
        messages.success(
            request, ("An account has been created and you are logged in.")
        )
        return redirect("dashboard")
        return redirect("dashboard")


class Login(View):
    def get(self, request: HttpRequest):
        return render(request, "login.html")

    def post(self, request: HttpRequest):
        form = request.POST
        email = form["email"]
        password = form["password"]

        user = authenticate(request, username=email, password=password)
        print(user)
        if user is None:
            messages.error(request, ("There was error signing you in."))
            return redirect("login")
        login(request, user)
        messages.success(request, ("Login Successful"))
        return redirect("dashboard")
        return redirect("dashboard")


def logout_user(request: HttpRequest) -> HttpResponse:
    messages.success(request, ("Signed out"))
    logout(request)
    return redirect("login")
