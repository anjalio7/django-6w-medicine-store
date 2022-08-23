from django.shortcuts import render

from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required

from sliced.models import user, Diseases, Medicine, Order

# Create your views here.
def index(request):
    if request.user != 'AnonymousUser':
        request.session["cart"] = []
    return render (request,'user_module/home.html')



def login_view(request):
    if request.method == "POST":
        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username,
        password=password)
        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "user_module/login.html", {
            "message": "Invalid username and/or password."
        })
    else:
        return render(request, "user_module/login.html")

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('userLogin'))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "user_module/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            users = user.objects.create_user(username, email, password)
            users.save()
        
        except IntegrityError:
            return render(request, "user_module/register.html", {
                "message": "Username already taken."
            })
        return render(request, 'user_module/register.html', {"message": 'Registered successfully.'})
    else:
        return render(request, "user_module/register.html")


def getMedicine(request, disId):
    selDis = Diseases.objects.get(id = disId)
    medData = Medicine.objects.filter(Disease_id = selDis)
    return render(request, 'user_module/medicines.html', {'medData': medData})

def viewMedDetail(request, medId):
    medData = Medicine.objects.get(id = medId)
    return render(request, 'user_module/medicineDetails.html', {'medData': medData})



@login_required(login_url='/user/userLogin')
def addToCart(request, medId):
    # a =  next((i for i,d in enumerate(request.session['cart']) if str(subId) in d), None)
    # print(a)
    # if a:
    #     print('yay')
    #     request.session['cart'][a][str(subId)] = request.session['cart'][a][str(subId)] + 1
    #     print(request.session['cart'])

    # else:
    #     b = dict()
    #     b[subId] = 1
    #     request.session['cart'] += [b]
    #     print(request.session['cart'])
    # data = sub_services.objects.get(id = subId)
    request.session['cart'] += [medId]
    # disId = Medicine.objects.get(id = medId).Disease_id.id
    return HttpResponseRedirect(reverse('viewMedDetail', kwargs={'medId': medId}))



@login_required(login_url='/user/userLogin')
def viewCart(request):
    # print(request.session['cart'])
    if len(request.session['cart']) > 0:
        # print(request.session['cart'])
        uniqueItem = list(set(request.session['cart']))
        print(uniqueItem)
        a = []
        sums = 0
        for i in uniqueItem:
            cartDict = dict()
            cartDict['item'] = Medicine.objects.get(id = i)
            cartDict['quant'] = request.session['cart'].count(i)
            cartDict['total'] = int(Medicine.objects.get(id = i).Price) * int(cartDict['quant'])
            sums += cartDict['total']
            a.append(cartDict)
        
        print(a)


        return render(request, 'user_module/viewCart.html', {'cart': a, 'checkout': sums})
    else:
        return render(request, 'user_module/viewCart.html', {'msg': 'Empty Cart'})

def removeItemCart(request, id):
    a = request.session['cart']
    a = list(filter((id).__ne__, a))
    print(a)
    request.session['cart'] = a

    return HttpResponseRedirect(reverse('viewCart'))

def allOrders(request):
    data = Order.objects.filter(user_id = request.user).order_by('orderDate')
    return render(request, 'user_module/allOrders.html', {'data': data})

def checkOut(request):
    try:
        if request.method == 'POST':
            address = request.POST['address']
        for i in list(set(request.session['cart'])):
            b = Medicine.objects.get(id = i)
            quan = int(request.session['cart'].count(i))
            prices = int(request.session['cart'].count(i)) * int(b.Price)
            a = Order(user_id = request.user, medicineId = b, address = address, quantity = quan, totalCost = prices)
            a.save()
        request.session['cart'] = []
        return HttpResponseRedirect(reverse('allOrders'))
    except:
        return HttpResponseRedirect(reverse('index'))