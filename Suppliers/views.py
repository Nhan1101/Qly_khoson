from django.shortcuts import render

# Create your views here.
def supplier_list(request):
    return render(request, 'suppliers/supplier_list.html')
