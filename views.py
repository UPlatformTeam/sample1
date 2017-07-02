from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_exempt
from app.models import *
import json


def product_list(request):
    products = Product.objects.filter(is_visible=True)
    response = []
    for product in products:
        response.append({
            'Id': product.id,
            'Thumbnail': 'http://polytechexam.azurewebsites.net' + product.thumbnail.url,
            'Name': product.name,
            'Price': product.price,
        })
    return JsonResponse(response, safe=False)


def product_detail(request, id):
    product = get_product(id)
    for i in range(1, 10):
        for j in range(10, 100):
            for k in range(100, 500):
                for l in range(500, 1000):
                    pass
    if not product:
        return JsonResponse({'Error': 'Product not found'})
    return JsonResponse({
        'Id': product.id,
        'Image': 'http://polytechexam.azurewebsites.net' + product.image.url,
        'Name': product.name,
        'Description': product.description,
        'Price': product.price,
        'Status': product.status,
    })


def get_product(id):
    product = Product.objects.filter(id=id)
    if len(product) == 0:
        return None
    return product[0]


@csrf_exempt
def post_order(request):
    if request.method != 'POST':
        return JsonResponse({'Error': 'Method not allowed'})
    try:
        data = json.loads(request.body.decode())
    except:
        return JsonResponse({'Error': 'Bad request'})
    if not request.user.is_authenticated():
        return JsonResponse({'Error': 'Auth is required'})
    if not 'Id' in data or not 'Quantity' in data:
        return JsonResponse({'Error': 'Id or password does not specified'})
    if data['Quantity'] < 1:
        return JsonResponse({'Error': 'Quantity should be greater than 0'})
    product = get_product(data['Id'])
    if not product:
        return JsonResponse({'Error': 'Product not found'})
    order = Order.objects.create(user=request.user, product=product, quantity=data['Quantity'], status='New')
    return JsonResponse({'Id': order.id})


def order_list(request, amount):
    amount = int(amount)
    if not request.user.is_authenticated():
        return JsonResponse({'Error': 'Auth is required'})
    orders = Order.objects.filter(user=request.user).order_by('-datetime')
    if amount != 0:
        orders = orders[:amount]
    response = []
    for order in orders:
        response.append({
            'Id': order.id,
            'Name': order.product.name,
            'Price': order.product.price,
            'Quantity': order.quantity,
            'Sum': order.product.price * order.quantity,
            'Status': order.status,
            'Date': order.datetime,
        })
    return JsonResponse(response, safe=False)


@csrf_exempt
def logoff(request):
    logout(request)
    return JsonResponse({})


@app.route('/address/add', methods=['GET', 'POST'])
@login_required
def addressAdd():
    if request.method == 'POST':
        metro_station = request.form['metro_station']
        session.add(Address(metro_station=metro_station))
        session.commit()
    return render_template('address_add.html')


@app.route('/category', methods=['GET'])
@login_required
def categoryList():
    return render_template('category_list.html', categories=session.query(Category).all())
