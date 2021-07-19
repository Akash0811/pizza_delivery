from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from .models import Order , RegularPizza , SicilianPizza , Sub , DinnerPlatter , Pasta , Salad , Topping ,\
        DisplayRegularPizza , DisplaySicilianPizza , DisplaySub , DisplayDinnerPlatter , DisplayPasta , DisplaySalad, DisplayTopping

# adds item to cart
def index(request , order_id):
    if not request.user.is_authenticated:
        return render(request, "orders/login.html", {"message": None})
    order = Order.objects.get(pk = order_id)
    content = {
        "order_id": order.id,
        "regular_pizza": order.regular_dish.all(),
        "sicilian_pizza": order.sicilian_dish.all(),
        "sub": order.subs0_dish.all(),
        "pasta": order.pasta_dish.all(),
        "salad": order.salad_dish.all(),
        "dinner_platter": order.dinnerplatter_dish.all(),
        "total": float("{0:.2f}".format(order.price))
    }
    return render( request , "orders/index.html" , content  )

# Menu in Login Page
def loginmenu(request):
    if request.user.is_authenticated:
        order = Order.objects.filter( user = request.user ).last()
        if not order:
            order = Order.objects.create( user = request.user )
            return menu(request, order.id)
        elif order.buy:
            order = Order.objects.create( user = request.user )
            return menu(request, order.id) 
        else:
            return menu(request, order.id) 
    context = {
        "RegularPizza": DisplayRegularPizza.objects.all(),
        "SicilianPizza": DisplaySicilianPizza.objects.all(),
        "Sub": DisplaySub.objects.all(),
        "Pasta": DisplayPasta.objects.all(),
        "Salad": DisplaySalad.objects.all(),
        "DinnerPlatter": DisplayDinnerPlatter.objects.all()
    }
    return render(request, "orders/loginmenu.html", context)

# Create your views here.
def menu(request , order_id):
    if not request.user.is_authenticated:
        return render(request, "orders/login.html", {"message": None})
    order = Order.objects.get(pk = order_id)
    context = {
        "user": request.user,
        "order_id": order.id,
        "RegularPizza": DisplayRegularPizza.objects.all(),
        "SicilianPizza": DisplaySicilianPizza.objects.all(),
        "Sub": DisplaySub.objects.all(),
        "Pasta": DisplayPasta.objects.all(),
        "Salad": DisplaySalad.objects.all(),
        "DinnerPlatter": DisplayDinnerPlatter.objects.all()
    }
    return render(request, "orders/menu.html", context)

# Confirm order
def view(request , order_id):
    if not request.user.is_authenticated:
        return render(request, "orders/login.html", {"message": None})
    order = Order.objects.get(pk = order_id)
    order.buy = True
    #confirmed = Confirmed_Order( order = order )
    order.save()
    #confirmed.save()
    logout(request)
    return render( request , "orders/login.html" , {"message": "Order Placed"}  )

# Creates new objects
def login_view(request):
    if request.method == 'GET':
        return render(request, "orders/login.html")
    username = request.POST["username"]
    password = request.POST["password"]
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        order = Order.objects.filter( user = request.user ).last()
        if not order:
            order = Order.objects.create( user = request.user )
        elif order.buy:
            order = Order.objects.create( user = request.user )
        return HttpResponseRedirect(reverse("index", args=(order.id,)))
    else:
        return render(request, "orders/login.html", {"message": "Invalid credentials."})

def register(request):
    logout(request)
    if request.method == 'GET':
        return render(request, "orders/register.html")
    username = request.POST["username"]
    password = request.POST["password"]
    email = request.POST["email"]
    first_name = request.POST["first_name"]
    last_name = request.POST["last_name"]
    if not username or not password or not email or not first_name or not last_name:
        return render(request, "orders/register.html", {"message": "Please fill Entire Form"})
    elif request.POST["password"] != request.POST["confirm_password"]:
        return render(request, "orders/register.html", {"message": "Passwords Mismatched"})
    user = User.objects.create_user(username , email , password )
    user.first_name = first_name
    user.last_name = last_name
    user.save()
    if user is not None:
        return render(request, "orders/login.html", {"message": None})
    else:
        return render(request, "orders/register.html", {"message": "Please fill Entire Form"})

# dish_id is special or regular
# order corresponds to which user order

@login_required
def regular_pizza(request , dish_id , order_id ):
    order = Order.objects.get( pk = order_id )
    if request.method == 'GET' :
        context = {
            "order_id": order_id,
            "dish_id": dish_id,
            "Topping": DisplayTopping.objects.all()
        }
        return render( request , "orders/regular_pizza.html" , context)
    try:
        size = request.POST["size"]
    except Exception:
        context = {
            "order_id": order_id,
            "dish_id": dish_id,
            "Topping": DisplayTopping.objects.all(),
            "message": "Please enter Size --  Small/Large"
        }
        return render( request , "orders/regular_pizza.html" , context)

    template = DisplayRegularPizza.objects.get( pk = dish_id )
    pizza = RegularPizza.objects.create( name = template.name ,
                                        SmallPrice = template.SmallPrice,
                                        LargePrice = template.LargePrice,
                                        Topping1SmallPrice = template.Topping1SmallPrice,
                                        Topping2SmallPrice = template.Topping2SmallPrice,
                                        Topping3SmallPrice = template.Topping3SmallPrice,
                                        Topping1LargePrice = template.Topping1LargePrice,
                                        Topping2LargePrice = template.Topping2LargePrice,
                                        Topping3LargePrice = template.Topping3LargePrice)
    count = 0
    for topping in DisplayTopping.objects.all():
        #print(request.POST[topping.name])
        if request.POST[topping.name] == 'Yes':
            topping = Topping.objects.create( name = topping.name)
            pizza.toppings.add(topping)
            count += 1
    pizza.no_of_toppings = count
    pizza.orders.add(order)
    if size == "Small":
        if pizza.price() == None:
            order.price += template.SmallPrice
        else:
            order.price += pizza.price()
        pizza.save()
        order.save()
        return HttpResponseRedirect(reverse("menu", args=(order_id,)))
    else:
        pizza.size = True
        if pizza.price() == None:
            order.price += template.LargePrice
        else:
            order.price += pizza.price()
        pizza.save()
        order.save()
        return HttpResponseRedirect(reverse("menu", args=(order_id,)))

@login_required
def sicilian_pizza(request , dish_id , order_id ):
    order = Order.objects.get( pk = order_id )
    if request.method == 'GET':
        context = {
            "order_id": order_id,
            "dish_id": dish_id,
            "Topping": DisplayTopping.objects.all()
        }
        return render( request , "orders/sicilian_pizza.html" , context)
    try:
        size = request.POST["size"]
    except Exception:
        context = {
            "order_id": order_id,
            "dish_id": dish_id,
            "Topping": DisplayTopping.objects.all(),
            "message": "Please enter Size --  Small/Large"
        }
        return render( request , "orders/sicilian_pizza.html" , context)
    template = DisplaySicilianPizza.objects.get( pk = dish_id )
    pizza = SicilianPizza.objects.create( name = template.name ,
                                        SmallPrice = template.SmallPrice,
                                        LargePrice = template.LargePrice,
                                        Topping1SmallPrice = template.Topping1SmallPrice,
                                        Topping2SmallPrice = template.Topping2SmallPrice,
                                        Topping3SmallPrice = template.Topping3SmallPrice,
                                        Topping1LargePrice = template.Topping1LargePrice,
                                        Topping2LargePrice = template.Topping2LargePrice,
                                        Topping3LargePrice = template.Topping3LargePrice)
    count = 0
    for topping in DisplayTopping.objects.all():
        #print(request.POST[topping.name])
        if request.POST[topping.name] == 'Yes':
            topping = Topping.objects.create( name = topping.name)
            pizza.toppings.add(topping)
            count += 1
    pizza.no_of_toppings = count
    pizza.orders.add(order)
    if size == "Small":
        if pizza.price() == None:
            order.price += template.SmallPrice
        else:
            order.price += pizza.price()
        pizza.save()
        order.save()
        return HttpResponseRedirect(reverse("menu", args=(order_id,)))
    else:
        pizza.size = True
        if pizza.price() == None:
            order.price += template.LargePrice
        else:
            order.price += pizza.price()
        pizza.save()
        order.save()
        return HttpResponseRedirect(reverse("menu", args=(order_id,)))

@login_required
def sub(request , dish_id , order_id ):
    order = Order.objects.get( pk = order_id )
    if request.method == 'GET':
        context = {
            "order_id": order_id,
            "dish_id": dish_id
        }
        return render( request , "orders/sub.html" , context)
    try:
        size = request.POST["size"]
    except Exception:
        context = {
            "order_id": order_id,
            "dish_id": dish_id,
            "message": "Please enter Size --  Small/Large"
        }
        return render( request , "orders/sub.html" , context)
    Xcheese = request.POST["Xcheese"]
    template = DisplaySub.objects.get( pk = dish_id )
    sub = Sub.objects.create( name = template.name,
                            SmallPrice = template.SmallPrice,
                            LargePrice = template.LargePrice,
                            XCheesePrice = template.XCheesePrice)
    sub.orders.add(order)
    if Xcheese == "Yes":
        sub.Xcheese = True
    if size == "Small":
        if sub.SmallPrice == None:
            context = {
                "order_id": order_id,
                "dish_id": dish_id,
                "message":"Small Size NOT Available"
            }
            return render( request , "orders/sub.html" , context)
        order.price += sub.price()
        sub.save()
        order.save()
        return HttpResponseRedirect(reverse("menu", args=(order_id,)))
    else:
        sub.size = True
        if sub.LargePrice == None:
            context = {
                "order_id": order_id,
                "dish_id": dish_id,
                "message":"Large Size NOT Available"
            }
            return render( request , "orders/sub.html" , context)
        order.price += sub.price()
        sub.save()
        order.save()
        return HttpResponseRedirect(reverse("menu", args=(order_id,)))

@login_required
def rest(request , type_id , dish_id , order_id ):
    order = Order.objects.get( pk = order_id )
    if request.method == 'GET':
        context = {
            "order_id": order_id,
            "dish_id": dish_id,
            "type_id": type_id
        }
        return render( request , "orders/rest.html" , context)
    if type_id ==1:
        template = DisplayPasta.objects.get( pk = dish_id )
        pasta = Pasta.objects.create( name = template.name,
                                    SmallPrice = template.SmallPrice)
        pasta.orders.add(order)
        order.price += pasta.SmallPrice
        pasta.save()
        order.save()
        return HttpResponseRedirect(reverse("menu", args=(order_id,)))
    elif type_id ==2:
        template = DisplaySalad.objects.get( pk = dish_id )
        salad = Salad.objects.create( name = template.name ,
                                    SmallPrice = template.SmallPrice)
        salad.orders.add(order)
        order.price += salad.SmallPrice
        salad.save()
        order.save()
        return HttpResponseRedirect(reverse("menu", args=(order_id,)))
    elif type_id == 3:
        template = DisplayDinnerPlatter.objects.get( pk = dish_id )
        dinner = DinnerPlatter.objects.create( name = template.name,
                                                SmallPrice = template.SmallPrice,
                                                LargePrice = template.LargePrice)
        dinner.orders.add(order)
        order.price += dinner.price()
        dinner.save()
        order.save()
        return HttpResponseRedirect(reverse("menu", args=(order_id,)))
    else:
        template = DisplayDinnerPlatter.objects.get( pk = dish_id )
        dinner = DinnerPlatter.objects.create( name = template.name,
                                                SmallPrice = template.SmallPrice,
                                                LargePrice = template.LargePrice)
        dinner.size = True
        dinner.orders.add(order)
        order.price += dinner.price()
        dinner.save()
        order.save()
        return HttpResponseRedirect(reverse("menu", args=(order_id,)))

def logout_view(request):
    logout(request)
    return render(request, "orders/login.html", {"message": "Logged out."})

'''
View orders wich have buy == True
Too complicated for use in admin.py
'''
@login_required
def confirmed_orders( request ):
    if request.user.is_superuser:
        context = {
            "orders": Order.objects.filter( buy = True ).all()
        }
        return render(request, "orders/confirmed_orders.html", context )
    else:
        logout(request)
        return render(request, "orders/login.html", {"message": "Forbidden"})
