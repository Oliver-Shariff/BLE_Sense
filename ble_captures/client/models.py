from django.db import models
from datetime import date
from django.contrib.auth.models import User

# the naming convention for django classes to that there are singular
#    the is because you will be querying them like so
# ```
# User.objects.all()
# ```

from dataclasses import dataclass
from datetime import date, timedelta


# Defining the Attack dataclass for testing
@dataclass
class Attack:
    id: int
    level: str
    sensor: int
    date: date
    CID: int


attack1 = Attack(1, "high", 10, date.today(), 1111)
attack2 = Attack(2, "medium", 20, date.today(), 2222)
attack3 = Attack(3, "low", 30, date.today() - timedelta(days=1), 3333)
attack4 = Attack(4, "high", 10, date.today(), 1111)
attack5 = Attack(5, "medium", 20, date.today(), 2222)
attack6 = Attack(6, "low", 30, date.today() - timedelta(days=2), 3333)
attack7 = Attack(7, "high", 10, date.today(), 1111)
attack8 = Attack(8, "medium", 20, date.today(), 2222)
attack9 = Attack(9, "low", 30, date.today() - timedelta(days=3), 3333)

# List of all instances
attacks = [
    attack1,
    attack2,
    attack3,
    attack4,
    attack5,
    attack6,
    attack7,
    attack8,
    attack9,
]


class Company(models.Model):
    __tablename__ = "Companies"
    name = models.TextField()

    registries: models.QuerySet["Registy"]


# grouper for user to register with many companies
#   and companies to have many users
class Registy(models.Model):
    __tablename__ = "Registers"
    password = models.TextField()

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="registries")
    company = models.ForeignKey(
        Company, on_delete=models.CASCADE, related_name="registries"
    )


class Group(models.Model):
    __tablename__ = "Groups"
    name = models.TextField()

    scanners: models.QuerySet["Scanner"]


class Scanner(models.Model):
    __tablename__ = "Scanners"
    name = models.TextField()

    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name="scanners")
    company = models.ForeignKey(
        Company, on_delete=models.CASCADE, related_name="scanners"
    )

    packets: models.QuerySet["Packet"] #One to many


class Packet(models.Model):
    __tablename__ = "Packets"
    mac_address = models.TextField()
    mac_frequencey = models.FloatField()
    company = models.TextField()
    # TODO: dicuss this
    #   should this be time since the recording started?
    #           -- how would we even get that?
    #   should this be time since Epoch?
    timestamp = models.DateField()

    
    scanner = models.ForeignKey(Scanner, on_delete=models.CASCADE)

class Device(models.Model):
    __tablename__ = "Devices"
    id = models.IntegerField()
    name = models.TextField(null="Unknown")
    oui = models.TextField(null="Unknown")

class Uuid(models.Model):
    __tablename__ = "UUIDs"
    uuid = models.IntegerField()

    device = models.ForeignKey(Device, on_delete=models.CASCADE)

class User(models.Model):
    __tablename__ = "Users"
    id = models.IntegerField()
    user_name = models.TextField()
    user_password = models.TextField()

class Scans(models.Model):
    __tablename__ = "Scans"
    scanner = models.ForeignKey(Scanner, on_delete=models.CASCADE)
    packet = models.ForeignKey(Packet, on_delete=models.CASCADE)

class Heartbeat(models.Model):
    __tablename__ = "Heartbeats"
    scanner = models.ForeignKey(Scanner, on_delete=models.CASCADE)
    used_mem = models.FloatField()
    total_mem = models.FloatField()
    used_swap = models.FloatField()
    total_swap = models.FloatField()
    serial_num = models.IntegerField()
    timestamp = models.DateField()
    total_cpu = models.FloatField()
    disk_info = models.ExpressionList() #Is this right?
    queue_length = models.IntegerField()