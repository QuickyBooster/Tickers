from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinLengthValidator

"""
•	Table user
id (primary key)
email(unique)
password (encrypted?? Or hash ??)
name
dob
phone
date_created
award_point
"""


class User(AbstractUser):
    username = models.EmailField(unique=True, null=True)
    name = models.CharField(max_length=20, blank=True)
    dob = models.DateField(null=True)
    phone = models.CharField(
        max_length=10,
        validators=[MinLengthValidator(10, "Phone number contains 10 numbers!")],
        unique=True,
        blank=False,
        null=True,
        default="0123456789",
    )
    date_created = models.DateTimeField(auto_now=True)
    award_point = models.IntegerField(null=True)
    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = []


"""
•	Table organizer
id (primary key)
commission_rate
total_revenue
detail
tax_code
head_office_address
legal_representative
phone_number
logo
"""


class Organizer(models.Model):
    name = models.CharField(max_length=70)
    commissison_rate = models.DecimalField(decimal_places=4, max_digits=5)
    total_revenue = models.DecimalField(decimal_places=3, max_digits=10, null=True)
    detail = models.TextField(max_length=500)
    tax_code = models.CharField(
        max_length=10,
        validators=[
            MinLengthValidator(10, "This field must contain at least 10 chars")
        ],
    )
    head_office_address = models.TextField(max_length=120)
    legal_representative = models.CharField(max_length=20)
    phone_number = models.CharField(
        max_length=10,
        validators=[MinLengthValidator(10, "Phone number must be 10 numbers")],
    )
    logo = models.ImageField(null=True, default="logo.png")

    class Meta:
        ordering = ["-name"]

    def __str__(self):
        return self.name


"""
•	Table event
id (primary key)
name
organizer (foreign key)
date (include time)
location_name
location_address
picture_master
picture_panel
detail
detail_picture
tag
"""


class Event(models.Model):
    name = models.CharField(max_length=70)
    organizer = models.ForeignKey(
        Organizer,
        on_delete=models.CASCADE,
        related_name="events",
    )
    date = models.DateTimeField()
    location_name = models.CharField(max_length=120,null=True)
    location_address = models.TextField(max_length=120)
    picture_master = models.ImageField(null=True, default="logo.png")
    picture_panel = models.ImageField(null=True, default="images/logo.png")
    detail = models.TextField(max_length=700, null=True)
    detail_picture = models.ImageField(null=True, default="images/logo.png")
    tag = models.CharField(max_length=10)

    class Meta:
        ordering = ["date", "-location_name"]

    def __str__(self):
        return self.name


"""
•	Table ticket_type
id (primary key)
event (foreign key)
type
price
quantity
"""


class TicketType(models.Model):
    event = models.ForeignKey(
        Event, on_delete=models.CASCADE, related_name="ticket_types"
    )
    type = models.CharField(max_length=30)
    price = models.IntegerField()
    quantity = models.IntegerField()

    class Meta:
        ordering = ["-event", "-price"]

    def __str__(self):
        return str(self.event.name + "_" + self.type)


"""
•	Table receipt
id (primary key)
user (foreign key)
total
date
transfer_id
status
"""


class Receipt(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    total = models.DecimalField(decimal_places=3, max_digits=12)
    date = models.DateTimeField(auto_now_add=True, blank=False)
    transfer_id = models.BigIntegerField(blank=False)

    class Meta:
        ordering = ["-date"]

    def __str__(self):
        return str(self.transfer_id)


"""
•	Table ticket
id (primary key)
ticket_type (foreign key)
user (foreign key)
seat
receipt
"""


class Ticket(models.Model):
    ticket_type = models.ForeignKey(TicketType, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='ticket_bought')
    seat = models.CharField(max_length=5)
    receipt = models.ForeignKey(
        Receipt, on_delete=models.CASCADE, related_name="tickets"
    )

    class Meta:
        ordering = ["-ticket_type", "-seat"]

    def __str__(self):
        return str(self.seat)


"""
Feedback
user (primary key)
eventid (primary key)
rating
comment
"""


class Feedback(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,null=True)
    event = models.ForeignKey(Event, on_delete=models.CASCADE,null=True)
    rating = models.IntegerField(null=True)
    comment = models.TextField(max_length=200,null=True)

    class Meta:
        ordering = ["-event", "-user"]

    def __str__(self):
        return str(self.event + "_" + self.user.username)


class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.TextField()
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-updated", "-created"]

    def __str__(self):
        return self.body[0:50]

class PendingPayment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tickets = models.ManyToManyField(Ticket, related_name="pending_payments")
    receipt = models.ForeignKey(Receipt, on_delete=models.CASCADE, related_name="pending_payments")
    status = models.CharField(max_length=20, default='Pending')

    def __str__(self):
        return f"{self.user.username}'s Payment - {self.status}"