from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    organiser = models.BooleanField(default=False)
    # 'Group' instead of Group as it is not defined yet
    group = models.ManyToManyField('Group', related_name="user_group", null=True, blank=True)

    def __str__(self):
        return f"Organiser: {self.organiser}, Group:{self.group}"


class Group(models.Model):
    title = models.CharField(max_length=64, null=True)
    members = models.ManyToManyField(User, blank=True, related_name="user_member")
    organiser = models.ForeignKey(User, on_delete=models.CASCADE, related_name="group_organizer")
    number_of_participants = models.IntegerField(default=0)
    exchange_date = models.DateTimeField()
    note = models.TextField(blank=True, null=True)
    budget = models.DecimalField(max_digits=10, decimal_places=2)
    shuffled = models.BooleanField(default=False)
    

    def __str__(self):
        return f"Title: {self.title}, Members: {self.members} ,Organiser:{self.organiser}, Number of participants: {self.number_of_participants}, Exchange Date: {self.exchange_date}, Note: {self.note}, Budget: {self.budget}"


class Category(models.Model):
    category = models.CharField(max_length=64, null=True)
    def __str__(self):
        return f"{self.category}"


class Gift(models.Model):
    title = models.CharField(max_length=64, null=True)
    image_url = models.URLField(default='google.com')
    category = models.ManyToManyField(Category, blank=True, related_name="gift_category")
    description = models.TextField(blank=True, null=True)
    likes = models.IntegerField(default=0)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    

    def serialize(self):
        return {
            "title":self.title,
            "image_url":self.image_url,
            "description":self.description,
            "likes":self.likes,
            "price":self.price,

        }

    def __str__(self):
        return f"Title:{self.title}, Category:{self.category}, Description: {self.description}, Likes: {self.likes}, Price: {self.price}"

class WishList(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name="wishlist_group")
    giftee = models.ForeignKey(User, on_delete=models.CASCADE, related_name="wishlist_giftee") 
    gifter = models.ForeignKey(User, on_delete=models.CASCADE, related_name="wishlist_gifter")
    gifts = models.ManyToManyField(Gift, blank=True, null=True, related_name="wishlist_gifts")
    note = models.TextField(blank=True, null=True)


    def __str__(self):
        return f"Giftee: {self.giftee}, Gifter: {self.gifter}, Gifts: {self.gifts}, Note:{self.note} "




class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_like") 
    gift = models.ForeignKey(Gift, on_delete=models.CASCADE, related_name="gift_like") 
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name="group_like", null=True)

    def serialize(self):
        return {
            "user":self.user.username,
            "gift":self.gift,
            "group":self.group
        }


    def __str__(self):
        return f"Username: {self.user.username}, Gift:{self.gift}"


class Alert(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="alert_user") 
    message = models.TextField(blank=True, null=True)
    read = models.BooleanField(default=False)
    group = models.CharField(max_length=64, blank=True, null=True)

    def serialize(self):
        return {
            "user":self.user.username,
            "message":self.message,
            "read":self.read,
            "group":self.group
        }


    def __str__(self):
        return f"Username: {self.user.username}, Message:{self.message}, Read: {self.read}, Group: {self.group}"

