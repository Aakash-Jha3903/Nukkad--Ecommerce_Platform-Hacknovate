
from django.db.models import Max, Min
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect, HttpResponse

from app.models import Slider
from app.models import BannerArea

from app.models import *
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.template.loader import render_to_string

from django.contrib.auth.decorators import login_required


def BASE(request):
    return render(request, 'base.html')


def HOME(request):
    sliders = Slider.objects.all().order_by("-id")[0:3]
    banner_areas = BannerArea.objects.all().order_by("-id")

    # main_category = MainCategory.object.all()
    main_categorys = MainCategory.objects.all()

    products = Product.objects.filter(section__name="Today's HOT DEALS 🔥")
    # products_images = ProductImage.objects.all()

    context = {
        'sliders': sliders,
        'banner_areas': banner_areas,
        "main_categorys": main_categorys,
        "products": products,
        # "products_images":products_images,

    }
    return render(request, 'Main/home.html', context)


def Product_Details(request, slug):
    # products = Product.objects.filter(slug=slug)
    # if products:
    products = Product.objects.filter(slug=slug)
    if products.exists():
        products = Product.objects.get(slug=slug)
    else:
        return redirect("404")
    products = Product.objects.filter(slug=slug)

    product_add_info = get_object_or_404(Product, slug=slug)
    # it is class, but keep it in lowercase !!
    Views_additional_information = product_add_info.additionalinformation_set.all()

    context = {
        "products": products,
        # Fetching AdditionalInformation objects
        "Views_additional_information": Views_additional_information
    }
    return render(request, "product/product_detail.html", context)


def Error404(request):
    return render(request, 'errors/404.html')


def MyAccount(request):
    return render(request, 'account/my_account.html')


def Register(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")

        if User.objects.filter(username=username).exists():
            messages.error(
                request, "User is Already Exists ! \n Try another Username")
            return redirect("login")
        if User.objects.filter(email=email).exists():
            messages.error(
                request, "Email id is Already Exists ! \n Try another Email")
            return redirect("login")

        user = User(username=username, email=email)

        user.set_password(password)
        user.save()
        # return redirect("account/my_account")
        return redirect("login")
        # return HttpResponse("You are registered !")
    else:
        return HttpResponse("You not are registered, or \n An error occured !")


def Login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("home")
        else:
            messages.error(request, "Email and Password are invalid !")
            return redirect("login")

    # return render(request, "account/my_account.html")


@login_required(login_url="registration/login/")
def Profile(request):
    return render(request, "profile/profile.html")


@login_required(login_url="registration/login/")
def Profile_Update(request):
    if request.method == "POST":
        username = request.POST.get("username")
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        email = request.POST.get("email")
        password = request.POST.get("password")
        user_id = request.user.id

        user = User.objects.get(id=user_id)
        user.first_name = first_name
        user.last_name = last_name
        user.username = username
        user.email = email

        if password != None and password != "":
            user.set_password(password)
        user.save()
        messages.success(
            request, f"{username} your profile is Successfully Updated ! ")

        return redirect('profile')


def logout_view(request):
    logout(request)
    # Redirect to a specific URL after logout
    # Replace 'home' with the name of your desired URL pattern
    return redirect('home')


def About(request):
    return render(request, "Main/about.html")


def Contact(request):
    return render(request, "Main/contact.html")


def Product_Page(request):
    categorys = Category.objects.all()
    products = Product.objects.all()

    colors = Color.objects.all()

    min_price = Product.objects.all().aggregate(Min('price'))
    max_price = Product.objects.all().aggregate(Max('price'))

    ColorID = request.GET.get("colorID")
    brands = BrandName.objects.all()

    FilterPrice = request.GET.get('FilterPrice')

    if FilterPrice:
        Int_FilterPrice = int(FilterPrice)
        products = Product.objects.filter(
            price__lte=Int_FilterPrice)
    elif ColorID:
        products = Product.objects.filter(color=ColorID)
    else:
        products = Product.objects.all()

    # products = price_filtered_product
    context = {
        "categorys": categorys,
        "products": products,
        'min_price': min_price,
        'max_price': max_price,
        'FilterPrice': FilterPrice,
        "colors": colors,
        "brands": brands,
        # "price_filtered_product": price_filtered_product,
    }
    return render(request, "product/product.html", context)


def filter_data(request):
    categories = request.GET.getlist('category[]')
    brands = request.GET.getlist('brand[]')
    product_num = request.GET.getlist("product_num[]")
    # [1,2,3]                                                             []')
    brand = request.GET.getlist('brand[]')

    allProducts = Product.objects.all().order_by('-id').distinct()
    if len(categories) > 0:
        allProducts = allProducts.filter(Categories__id__in=categories).distinct()


    if len(product_num) > 0:
        allProducts = allProducts.all().order_by('-id')[0:1]

    # if len(brands) > 0:
    #     allProducts = allProducts.filter(Brand__id__in=brands).distinct()
    # if len(brands) > 0:
        # allProducts = allProducts.filter(brand_name__id__in=brands).distinct()
        
    if len(brands) > 0:
        allProducts = allProducts.filter(brand_name__id__in=brands).distinct()


    # if len(brand) > 0:
    #     allProducts = allProducts.filter()

    t = render_to_string('ajax/product.html',
                     {'product': allProducts})  # type: ignore

    return JsonResponse({'data': t})



# from store.models import Product
from django.contrib.auth.decorators import login_required
from cart.cart import Cart

@login_required(login_url="/account/profile")
def cart_add(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.add(product=product)
    return redirect("cart_detail")


@login_required(login_url="/account/profile")
def item_clear(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.remove(product)
    return redirect("cart_detail")


@login_required(login_url="/account/profile")
def item_increment(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.add(product=product)
    return redirect("cart_detail")


@login_required(login_url="/account/profile")
def item_decrement(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.decrement(product=product)
    return redirect("cart_detail")


@login_required(login_url="/account/profile")
def cart_clear(request):
    cart = Cart(request)
    cart.clear()
    return redirect("cart_detail")


@login_required(login_url="/account/profile")
def cart_detail(request):
    product = Product.objects.all()
    context = {
        "product": product,
    }
    return render(request, 'cart/cart.html')
    # return render(request, 'cart/cart.html',context)
    # return render(request, 'cart/cart_detail.html',context)