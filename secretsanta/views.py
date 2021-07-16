from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages


import random
from collections import deque


from . models import User, Group, Category, WishList, Gift, Like, Alert

import json





def index(request):
	return render(request, "secretsanta/index.html")


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("groups"))
        else:
            return render(request, "secretsanta/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "secretsanta/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        # username = request.POST.get('username')
        username = request.POST["username"]
        email = request.POST["email"]
        # email = request.POST.get("email")

        # Ensure password matches confirmation
        password = request.POST["password"]
        # password = request.POST.get("password")
        confirmation = request.POST["confirmation"]
        # confirmation = request.POST.get("confirmation")
        if password != confirmation:
            return render(request, "secretsanta/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "secretsanta/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("groups"))
    else:
        return render(request, "secretsanta/register.html")


def pairup(request, group_id):
    group_ind = Group.objects.get(pk=group_id)


    for mem in group_ind.members.all():
        if mem == group_ind.organiser:
            alert = Alert(
                    user=request.user,
                    message=f"You have shuffled the list for '{group_ind.title}'!",
                    read=False,
                    group=group_ind.title,
                    )
            alert.save()
        else:
            alert = Alert(
                    user=mem,
                    message=f"'{group_ind.title}' list has been shuffled! Check out your secret giftee!",
                    read=False,
                    group=group_ind.title,
                    )
            alert.save()

    arr = []
    for mem in group_ind.members.all():
        if mem not in arr:
            arr.append(mem)


    random.shuffle(arr)
    partners = deque(arr)
    partners.rotate()

    pairs = dict(zip(arr,partners))

    cat = Category.objects.get(category='General')



    for key, value in pairs.items():
            wishlist = WishList(
                group=group_ind,
                giftee=key,
                gifter=value,
                note='',
                )
            wishlist.save()



    group_ind.shuffled = True
    group_ind.save()
    return HttpResponseRedirect(reverse('group', args=[group_id]))



def choose(request):

    groups = Group.objects.all()
    users = User.objects.all()

    if request.method == 'POST':
        user = request.user
        names = request.POST.getlist('input')
        for name in names:
            if name == "":
                names.remove(name)
        

        group_name = request.POST["group_name"]
        date = request.POST["date"]
        budget = request.POST["budget"]
        message = request.POST["message"]

        group_names = []
        for gn in groups:
            group_names.append(gn.title.lower())

        if group_name.lower() not in group_names:

            group_ind = Group(
                title=group_name,
                organiser=user,
                exchange_date=date,
                note=message,
                budget=budget,
                shuffled=False
            )
            group_ind.save()

            existing_names = User.objects.all()

            for name in existing_names:
                for n in names:
                    if name.username == n:
                        if name not in group_ind.members.all():
                            group_ind.members.add(name)

            group_ind.members.add(user)
            group_ind.number_of_participants = len(group_ind.members.all())
            
            group_ind.save()

            # user.group = group

            for u in users:
                if u in group_ind.members.all():
                    u.group.add(group_ind)
            

            alert = Alert(
                    user=request.user,
                    message=f"You have added a new group called '{group_ind.title}'!",
                    read=False,
                    group=group_ind.title,
                    )
            alert.save()

            for mem in group_ind.members.all():
                if mem != request.user:
                    alert = Alert(
                        user=mem,
                        message=f"You have been added to a new group called '{group_ind.title}'!",
                        read=False,
                        group=group_ind.title,
                        )
                    alert.save()
        else:
            alert = Alert(
                    user=request.user,
                    message=f"Group name already existed! Please choose another name!",
                    read=False,
                    )
            alert.save()


        return HttpResponseRedirect(reverse('groups'))
        

        

    return render(request, "secretsanta/choose.html", {
            "user": request.user
        })

    

def groups(request):
    user = request.user
    groups = Group.objects.all()
    fil = user.group.all()
    alerts = Alert.objects.filter(user=user, read=False)


    users = User.objects.all()
    return render(request, "secretsanta/groups.html",{
            "groups": groups,
            "users": users,
            "user": user,
            "fil": fil,
            "alerts": alerts
        }
    )


def group(request,group_id):
    user = request.user
    group_info = Group.objects.get(pk=group_id)
    wishlist = WishList.objects.filter(group=group_info)
    title = group_info.title
    alerts = Alert.objects.filter(user=user,read=False, group=title)

    date = group_info.exchange_date
    date_str = date.strftime("%Y-%m-%d")
    members = []
    for mem in group_info.members.all():
        members.append(mem.username)

    return render(request, "secretsanta/group.html",{
            "group": group_info,
            "user": user,
            "wishlist": wishlist,
            "alerts": alerts,
            "exchange_date": date_str,
            "members": members
        });


def delete_group(request, group_id):
    group_ind = Group.objects.get(pk=group_id)
    user = request.user

    title = group_ind.title

    for mem in group_ind.members.all():
        if mem == user:
            alert = Alert(
                    user=mem,
                    message=f"You have deleted '{title}'! You will no longer be able to participate in that group's activity.",
                    read=False,
                    group=title,
                    )
            alert.save()
        else:
            alert = Alert(
                    user=mem,
                    message=f"{user.username} has deleted '{title}'! You will no longer be able to participate in that group's activity.",
                    read=False,
                    group=title,
                    )
            alert.save()
    Group.objects.get(pk=group_id).delete()

    return HttpResponseRedirect(reverse('groups'))



def leave_group(request, group_id):
    user = request.user
    user_group = Group.objects.get(pk=group_id)
    user.group.remove(user_group)
    user_group.members.remove(user)
    user_group.number_of_participants = len(user_group.members.all())
    user_group.save()

    alert = Alert(
                user=user,
                message=f"You have left '{user_group.title}'! You will no longer be able to participate in that group's activity.",
                read=False,
                group=user_group.title,
                )
    alert.save()

    # delete wishlist
    wishlist = WishList.objects.filter(group=user_group).delete()

    # Reshuffle to create new wishlist if shuffled already
    if user_group.shuffled:
        arr = []
        for mem in user_group.members.all():
            if mem not in arr:
                arr.append(mem)


        random.shuffle(arr)
        partners = deque(arr)
        partners.rotate()

        pairs = dict(zip(arr,partners))

        cat = Category.objects.get(category='General')

        for key, value in pairs.items():
                wishlist = WishList(
                    group=user_group,
                    giftee=key,
                    gifter=value,
                    note=''
                    )
                wishlist.save()
        # use alert model!!!
        for mem in user_group.members.all():
            alert = Alert(
                user=mem,
                message=f"{user.username} has left '{user_group.title}'! SecretSantas has reshuffled the list of names. Check out your new secret giftee!",
                read=False,
                group=user_group.title,

                )
            alert.save()

    else:
        for mem in user_group.members.all():
            alert = Alert(
                user=mem,
                message=f"{user.username} has left '{user_group.title}'!",
                read=False,
                group=user_group.title,
            )
            alert.save()

    return HttpResponseRedirect(reverse('groups'))




@csrf_exempt
def read(request, alert_id):

    alert = Alert.objects.get(id=alert_id)

    if request.method == "GET":
        return JsonResponse(post.serialize())


    if request.method == "PUT":
        data = json.loads(request.body)
        if data.get("read"):
            al = Alert.objects.get(pk=alert_id)
            al.read = True
            al.save()
            # Alert.objects.get(pk=alert_id).remove()
            
        return HttpResponse(status=204)  



def edit(request, group_id):

    if request.method == 'POST':
        user = request.user
        names = request.POST.getlist('mem')
        budget = request.POST.get('budget')
        exchange_date = request.POST.get('exchange_date')
        group_name = request.POST.get('group_name')
        note = request.POST.get('note')


        
        group_ind = Group.objects.get(pk=group_id)

        different = False


        group_members = []

        # compare if different, then add
        for mem in group_ind.members.all():
            if group_ind.organiser != mem:
                group_members.append(mem.username)
                if mem.username not in names:
                    different = True
                    # if existing member is kicked out
                    old_mem = User.objects.get(pk=mem.id)
                    r_group = old_mem.group.get(pk=group_id)
                    old_mem.group.remove(r_group)
                    # notif for organiser
                    alert_org = Alert(
                        user=user,
                        message=f"You have removed {mem.username} from {group_ind.title}.",
                        read=False,
                        group=group_ind.title,
                        )
                    alert_org.save()
                    alert = Alert(
                        user=mem,
                        message=f"You have been removed from {group_ind.title}. You will no longer be able to participate in that group's activity.",
                        read=False,
                        group=group_ind.title,
                        )
                    alert.save()


        for n in names:
            if len(User.objects.filter(username=n)):
                if n not in group_members and n != group_ind.organiser.username:
                    different = True
                    # if new member is added, new member will receive this notif
                    new_member = User.objects.get(username=n)
                    # new_member.group.add(group_ind)
                    alert_org = Alert(
                        user=user,
                        message=f"You have added {new_member.username} to {group_ind.title}!",
                        read=False,
                        group=group_ind.title,
                        )
                    alert_org.save()
                    alert = Alert(
                            user=new_member,
                            message=f"You have been added to {group_ind.title}!",
                            read=False,
                            group=group_ind.title,
                            )
                    alert.save()

        if different:
            for mem in group_ind.members.all():
                if mem != group_ind.organiser:
                    group_ind.members.remove(mem)

        for nm in names:
            if len(User.objects.filter(username=nm)):
                new_mem = User.objects.get(username=nm)
                new_mem.group.add(group_ind)
                group_ind.members.add(new_mem)
                group_ind.save()

        # if different, for all existing members, use this notif
        if different and group_ind.shuffled:
            for mem in group_ind.members.all():
                
                if mem == group_ind.organiser:
                    alert = Alert(
                        user=user,
                        message=f"You have changed {group_ind.title} list! SecretSantas has reshuffled the list of names. Check out your new secret giftee!",
                        read=False,
                        group=group_ind.title,
                        )
                    alert.save()

                else:
                    alert_mem = Alert(
                        user=mem,
                        message=f"{group_ind.title} list has been changed! SecretSantas has reshuffled the list of names. Check out your new secret giftee!",
                        read=False,
                        group=group_ind.title,
                        )
                    alert_mem.save()
        

        


        # if different, reshuffle and delete original wishlist
        if different and group_ind.shuffled:
            wishlists = WishList.objects.filter(group=group_ind).delete()
            arr = []
            for mem in group_ind.members.all():
                if mem not in arr:
                    arr.append(mem)
            random.shuffle(arr)
            partners = deque(arr)
            partners.rotate()

            pairs = dict(zip(arr,partners))

            cat = Category.objects.get(category='General')

            for key, value in pairs.items():
                    wishlist = WishList(
                        group=group_ind,
                        giftee=key,
                        gifter=value,
                        note=''
                        )
                    wishlist.save()

            group_ind.shuffled = True
            group_ind.save()

        
        groups = Group.objects.all()
        group_names = []
        for gn in groups:
            group_names.append(gn.title.lower())

        if str(group_ind.title) != str(group_name):
            if group_name.lower() not in group_names:
                for mem in group_ind.members.all():
                    alert = Alert(
                        user=mem,
                        message=f"Group name has been changed from {group_ind.title} to {group_name}!",
                        read=False,
                        group=group_name,
                        )
                    alert.save()
                group_ind.title = group_name
            else:
                alert = Alert(
                        user=user,
                        message=f"Group name already existed! Please choose another name!",
                        read=False,
                        group=group_ind.title
                        )
                alert.save()



        if str(group_ind.budget) != str(budget):
            for mem in group_ind.members.all():
                alert = Alert(
                    user=mem,
                    message=f"Group budget has been changed from {group_ind.budget} to {budget}!",
                    read=False,
                    group=group_ind.title,
                    )
                alert.save()

        if group_ind.exchange_date.strftime("%Y-%m-%d") != exchange_date:
            str_date = group_ind.exchange_date.strftime("%Y-%m-%d")
            for mem in group_ind.members.all():
                alert = Alert(
                    user=mem,
                    message=f"Exchange date  has been changed from {str_date} to {exchange_date}!",
                    read=False,
                    group=group_ind.title,
                    )
                alert.save()

        if group_ind.note != note:
            for mem in group_ind.members.all():
                alert = Alert(
                    user=mem,
                    message=f"{group_ind.note} has been changed to {note}!",
                    read=False,
                    group=group_ind.title,
                    )
                alert.save()


        
        group_ind.budget = budget
        group_ind.exchange_date = exchange_date
        group_ind.note = note
        group_ind.save()

    return HttpResponseRedirect(reverse('group',args=[group_id]))


def browse(request):

    categories = Category.objects.all()
    gifts = Gift.objects.all()
    toy_cat = Category.objects.get(category="Toys")
    toys = Gift.objects.filter(category=toy_cat)
    electronic_cat = Category.objects.get(category="Electronics")
    electronics = Gift.objects.filter(category=electronic_cat)
    fashion_cat = Category.objects.get(category="Fashion")
    fashion = Gift.objects.filter(category=fashion_cat)
    food_cat = Category.objects.get(category="Food")
    food = Gift.objects.filter(category=food_cat)

    user = request.user
    groups = user.group.all()



    wishlists = WishList.objects.filter(giftee=user)


    count = 0
    for l in wishlists:
        num = len(l.gifts.all())
        count += num

    wish_count = count


    likes = Like.objects.all()


    user_likes = Like.objects.filter(user=user)



    inside_likes_gift = []
    inside_likes_group = []
    inside_likes_user = []

    for like in likes:
        inside_likes_group.append(like.group)
        inside_likes_gift.append(like.gift)
        inside_likes_user.append(like.user)

    for gift in gifts:
        gift.likes = Like.objects.filter(gift=gift).count()
        gift.save()



    shuff = []
    unshuff = []
    shuffled = Group.objects.all()
    for g in shuffled:
        if g.shuffled:
            shuff.append(g)
        else:
            unshuff.append(g)



    return render(request, "secretsanta/browse.html",{
        "categories": categories,
        "gifts": gifts,
        "toys": toys,
        "electronics": electronics,
        "fashion": fashion,
        "food": food,
        "groups": groups,
        "wishlists": wishlists,
        "user": user,
        "shuff": shuff,
        "unshuff": unshuff,
        "likes": likes,
        "inside_likes_gift": inside_likes_gift,
        "inside_likes_group": inside_likes_group,
        "inside_likes_user": inside_likes_user,
        "user_likes": user_likes,
        "wish_count": wish_count
        })


@csrf_exempt
def like(request, gift_id, group_id):
    user = request.user
    gift = Gift.objects.get(pk=gift_id)
    group = Group.objects.get(pk=group_id)
    wishlist = WishList.objects.get(giftee=user, group=group)
    

    if request.method == "GET":
        return JsonResponse(gift.serialize())

    if request.method == "PUT":
        data = json.loads(request.body)
        if data.get("like"):
            Like.objects.create(user=request.user, gift=gift,group=group)
            gift.likes = Like.objects.filter(gift=gift).count()
            wishlist.gifts.add(gift)
    
        else: 
            Like.objects.filter(user=request.user, gift=gift, group=group).delete()
            gift.likes = Like.objects.filter(gift=gift).count()
            for g in wishlist.gifts.all():
                if g == gift:
                    wishlist.gifts.remove(g)

        gift.save()
        wishlist.save()
        return HttpResponse(status=204)  



@csrf_exempt
def edit_notes(request, wishlist_id):
    wishlist = WishList.objects.get(pk=wishlist_id)


    if request.method == "POST":
        message = request.POST["message"]

        wishlist.note = message
        wishlist.save()


        return HttpResponseRedirect(reverse('browse'))


    
