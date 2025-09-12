from django.shortcuts import render, redirect
from .models import Customer, Pictures
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .forms import CustomerForm
from django.http import JsonResponse
from .forms import PictureForm
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
today = timezone.now().date()
@login_required
def home(request):
    # customers = Customer.objects.filter(isdelete=False).order_by('-adddate')
    # pictures = Pictures.objects.filter(isDeleted=False).order_by('-adddate')
    customers = Customer.objects.filter(lastupdateuserid=request.user,
        isdelete=False,
        adddate__date=today
    ).order_by('adddate')
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
    ).order_by('adddate')
    first_group = request.user.groups.first()
    group_name = first_group.name if first_group else 'Không có nhóm'

    if request.method == 'POST':
        form = CustomerForm(request.POST)
        if form.is_valid():
            customer = form.save(commit=False)
            customer.lastupdateuserid = request.user
            customer.save()
            return redirect('create_customer')  # hoặc redirect đến danh sách khách hàng
    else:
        form = CustomerForm()
    return render(request, 'customer/create.html', {'form': form, 'customers': customers, 'group_name': group_name})

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
                    'note': customer.note,
                    'KHDV': customer.KHDV,
                    'CVDV': customer.CVDV,
                    'adddate': customer.adddate.isoformat() or '',
                }
            })
        else:
            return JsonResponse({'success': False, 'error': 'Dữ liệu không hợp lệ'})

@login_required
@csrf_exempt 
def get_customer_ajax(request, customer_id):
    try:
        customer = Customer.objects.get(id=customer_id)
        return JsonResponse({
            'success': True,
            'customer': {
                'id': customer.id,
                'name': customer.name,
                'plate': customer.plate,
                'note': customer.note,
                'adddate': customer.adddate.isoformat(),
                'KHDV': customer.KHDV,
                'CVDV': customer.CVDV,
            }
        })
    except Customer.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Không tìm thấy khách hàng.'})

@login_required
def update_customer_ajax(request, customer_id):
    if request.method == 'POST':
        try:
            customer = Customer.objects.get(id=customer_id)
        except Customer.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Khách hàng không tồn tại.'})

        form = CustomerForm(request.POST, instance=customer)
        if form.is_valid():
            updated_customer = form.save()
            return JsonResponse({
                'success': True,
                'customer': {
                    'id': updated_customer.id,
                    'name': updated_customer.name,
                    'plate': updated_customer.plate,
                    'note': updated_customer.note,
                    'adddate': updated_customer.adddate.isoformat(),
                    'KHDV': updated_customer.KHDV,
                    'CVDV': updated_customer.CVDV,
                }
            })
        else:
            return JsonResponse({'success': False, 'error': 'Dữ liệu không hợp lệ.', 'errors': form.errors})
    else:
        return JsonResponse({'success': False, 'error': 'Phương thức không hợp lệ.'})        

@login_required
def customer_list_ajax(request):
    customers = Customer.objects.filter(
        lastupdateuserid=request.user,
        adddate__date=today,
        isdelete=False
    ).order_by('adddate')

    data = [
        {
            'id': customer.id,
            'adddate': customer.adddate,
            'name': customer.name,
            'plate': customer.plate,
            'note': customer.note,
            'KHDV': customer.KHDV,
            'CVDV': customer.CVDV or '',
        }
        for customer in customers
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
    
@login_required
def delete_customer_ajax(request):
    customer_id = request.POST.get('id')
    try:
        customer = Customer.objects.get(id=customer_id, lastupdateuserid=request.user)
        customer.isdelete = True  # hoặc dùng .delete() nếu muốn xóa thật
        customer.save()
        return JsonResponse({'success': True})
    except Customer.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Khách hàng không tồn tại'})


