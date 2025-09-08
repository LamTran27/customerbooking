from django.shortcuts import render, redirect
from .models import Customer, Pictures
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .forms import CustomerForm
from django.http import JsonResponse
from .forms import PictureForm

# Create your views here.
today = timezone.now().date()
@login_required
def home(request):
    # customers = Customer.objects.filter(isdelete=False).order_by('-adddate')
    # pictures = Pictures.objects.filter(isDeleted=False).order_by('-adddate')
    customers = Customer.objects.filter(lastupdateuserid=request.user,
        isdelete=False,
        adddate__date=today
    ).order_by('-adddate')
    pictures = Pictures.objects.filter(
        lastupdateuserid=request.user,
        isDeleted=False
    ).order_by('-adddate')

    first_group = request.user.groups.first()
    group_name = first_group.name if first_group else 'Không có nhóm'
    return render(request, 'base/home.html', {'customers': customers, 'pictures': pictures, 'group_name': group_name})

@login_required
def create_customer(request):
    form = CustomerForm()
    customers = Customer.objects.filter(
        lastupdateuserid=request.user,
        isdelete=False,
        adddate__date=today
    ).order_by('-adddate')

    if request.method == 'POST':
        form = CustomerForm(request.POST)
        if form.is_valid():
            customer = form.save(commit=False)
            customer.lastupdateuserid = request.user
            customer.save()
            return redirect('home')  # hoặc redirect đến danh sách khách hàng
    else:
        form = CustomerForm()
    return render(request, 'customer/create.html', {'form': form, 'customers': customers})

@login_required
def create_customer_ajax(request):
    if request.method == 'POST':
        form = CustomerForm(request.POST)
        if form.is_valid():
            customer = form.save(commit=False)
            customer.lastupdateuserid = request.user
            customer.save()
            return JsonResponse({
                'success': True,
                'customer': {
                    'id': customer.id,
                    'name': customer.name,
                    'plate': customer.plate,
                    'note': customer.note or '',
                }
            })
        else:
            return JsonResponse({'success': False, 'error': 'Dữ liệu không hợp lệ'})
@login_required
def customer_list_ajax(request):
    customers = Customer.objects.filter(
        lastupdateuserid=request.user,
        isdelete=False
    ).order_by('-adddate')

    data = [
        {
            'name': c.name,
            'plate': c.plate,
            'note': c.note or '',
        }
        for c in customers
    ]
    return JsonResponse({'customers': data})

@login_required
def upload_picture(request):
    pictures = Pictures.objects.filter(
        lastupdateuserid=request.user,
        isDeleted=False
    ).order_by('-adddate')
    form = PictureForm()
    if request.method == 'POST':
        form = PictureForm(request.POST, request.FILES)
        if form.is_valid():
            picture = form.save(commit=False)
            picture.lastupdateuserid = request.user
            picture.save()
            return redirect('upload_picture')  # hoặc redirect đến trang hiển thị ảnh
    return render(request, 'pictures/upload.html', {'form': form, 'pictures': pictures})

@login_required
def delete_picture(request, pic_id):
    try:
        pic = Pictures.objects.get(id=pic_id, lastupdateuserid=request.user)
        pic.isDeleted = True
        pic.deletedDate = timezone.now()
        pic.save()
        return JsonResponse({'success': True})
    except Pictures.DoesNotExist:
        return JsonResponse({'success': False})


