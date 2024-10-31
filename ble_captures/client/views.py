from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from client.models import *
from django.views import View
from dataclasses import dataclass, asdict
from django.http import JsonResponse
from django.core.validators import EmailValidator
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import authenticate, login, logout
from django.core.exceptions import ValidationError
from django.contrib import messages
from django.contrib.auth.models import User


@dataclass
class Device:
    id: int
    name: str
    OUI: str
    comp_id: int
    group: str
    mal: bool


devices_dict = {
    1: Device(
        id=1,
        name="Router-X100",
        OUI="00:1A:2B",
        comp_id=101,
        group="Networking",
        mal=False,
    ),
    2: Device(
        id=2,
        name="Switch-S200",
        OUI="00:1A:3C",
        comp_id=102,
        group="Networking",
        mal=True,
    ),
    3: Device(
        id=3,
        name="AccessPoint-A300",
        OUI="00:1A:4D",
        comp_id=103,
        group="Wireless",
        mal=False,
    ),
    4: Device(
        id=4,
        name="Firewall-F400",
        OUI="00:1A:5E",
        comp_id=104,
        group="Security",
        mal=False,
    ),
    5: Device(
        id=5,
        name="Repeater-R500",
        OUI="00:1A:6F",
        comp_id=105,
        group="Networking",
        mal=True,
    ),
    6: Device(
        id=6,
        name="Modem-M600",
        OUI="00:1B:2A",
        comp_id=106,
        group="Networking",
        mal=False,
    ),
    7: Device(
        id=7, name="Hub-H700", OUI="00:1B:3B", comp_id=107, group="Networking", mal=True
    ),
    8: Device(
        id=8, name="Sensor-S800", OUI="00:1B:4C", comp_id=108, group="IoT", mal=False
    ),
    9: Device(
        id=9,
        name="Camera-C900",
        OUI="00:1B:5D",
        comp_id=109,
        group="Security",
        mal=True,
    ),
    10: Device(
        id=10,
        name="SmartLock-L1000",
        OUI="00:1B:6E",
        comp_id=110,
        group="IoT",
        mal=False,
    ),
}


def fetch_devices(request):
    # Convert each Device object in devices_dict to a dictionary
    device_data = {
        "devices": {key: asdict(device) for key, device in devices_dict.items()}
    }

    return JsonResponse(device_data, safe=False)


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


def packets(request: HttpRequest, device_id: int) -> HttpResponse:
    device = devices_dict.get(device_id)

    context = {"this_device": asdict(device)}

    JsonResponse(context, safe=False)
    # need to add packets object to this
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


def logout_user(request: HttpRequest) -> HttpResponse:
    messages.success(request, ("Signed out"))
    logout(request)
    return redirect("login")
