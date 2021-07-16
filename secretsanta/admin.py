from django.contrib import admin

from .models import User, Group, Category, WishList, Gift, Like, Alert


# Register your models here.
admin.site.register(User)
admin.site.register(Group)
admin.site.register(Category)
admin.site.register(WishList)
admin.site.register(Gift)
admin.site.register(Like)
admin.site.register(Alert)



