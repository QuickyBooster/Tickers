from django.db import models
from django.contrib.auth.models import AbstractUser

"""
•	Table user
o	id (primary key)
o	email (unique)
o	password (encrypted?? Or hash ??)
o	name
o	dob
o	phone
o	date_created
"""


class User(AbstractUser):
    username = models.EmailField(unique=True, null=True)
    name = models.CharField(max_length=20, blank=True)
    dob = models.DateField(null=True)
    phone = models.TextField(unique=True, blank=False, null=True)
    date_created = models.DateTimeField(auto_now=True)
    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = []


"""
•	Table organizer
o	id (primary key)
o	name 
o	detail
o	location
"""


class Organizer(models.Model):
    name = models.CharField(max_length=70, null=True)
    detail = models.TextField(max_length=500)
    location = models.TextField(max_length=120)

    class Meta:
        ordering = ["-name"]

    def __str__(self):
        return self.name


"""
•	Table event
o	id (primary key)
o	name
o	organizer (foreign key)
o	date (include time)
o	location
o	picture_master
o	picture_panel
o	detail
o	detail_picture

"""


class Event(models.Model):
    name = models.CharField(max_length=70, null=True)
    organizer = models.ForeignKey(Organizer, on_delete=models.CASCADE, null=True)
    date = models.DateTimeField(null=False)
    location = models.TextField(max_length=120)
    picture_master = models.ImageField(null=True, default="logo.png")
    picture_panel = models.ImageField(null=True, default="images/logo.png")
    detail = models.TextField(max_length=700, null=True)
    detail_picture = models.ImageField(null=True, default="images/logo.png")

    class Meta:
        ordering = ["-date", "-location"]

    def __str__(self):
        return self.name


"""
•	Table ticket_type
o	id (primary key)
o	event (foreign key)
o	type
o	price
o	quantity

"""


class TicketType(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, null=True)
    type = models.CharField(max_length=30, null=True)
    price = models.DecimalField(decimal_places=2, null=True, max_digits=12)
    quantity = models.IntegerField(null=True)

    class Meta:
        ordering = ["-event", "-price"]

    def __str__(self):
        return self.type


"""
•	Table ticket
o	id (primary key)
o	ticket_type (foreign key)
o	quantity
o	profile (foreign key)
o	total
"""


class Ticket(models.Model):
    ticket_type = models.ForeignKey(TicketType, on_delete=models.CASCADE, null=True)
    quantity = models.IntegerField(null=True)
    profile = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    total = models.DecimalField(decimal_places=2, null=True, max_digits=12)

    class Meta:
        ordering = ["-profile", "-total"]

    def __str__(self):
        return str(self.total)


"""
•	Table receipt
o	id (primary key)
o	ticket (foreign key) – [array]
o	profile (foreign key)
o	total
o	date
o	transfer_id
"""


class Receipt(models.Model):
    tickets = models.ManyToManyField(Ticket, related_name="tickets", blank=False)
    profile = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    total = models.DecimalField(decimal_places=2, null=True, max_digits=12)
    date = models.DateTimeField(auto_now_add=True, null=False, blank=False)
    transfer_id = models.BigIntegerField(blank=False)

    class Meta:
        ordering = ["-date"]

    def __str__(self):
        return str(self.transfer_id)
