from django.shortcuts import render,redirect
from .models import Item
from .forms import ItemForm
from django.contrib.auth.decorators import login_required
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView,UpdateView,DeleteView
from django.urls import reverse_lazy
from django.core.paginator import Paginator
from .serializers import ItemSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view
# Create your views here.

@api_view(["GET", "POST"])
def item_list_api(request):
    if request.method=="GET":
        items = Item.objects.all()
        serializer = ItemSerializer(items,many=True)
        return Response(serializer.data)
    elif request.method=="POST":
        serializer = ItemSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

@api_view(["GET","PUT"])
def item_detail_api(request,pk):
    item =  Item.objects.get(pk=pk)
    if request.method=="GET":
        serializer = ItemSerializer(item)
        return Response(serializer.data)
    elif request.method=="PUT":
        serializer = ItemSerializer(item,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

@login_required
def index(request):
    item_list = Item.objects.all()
    paginator = Paginator(item_list,5)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    context = {
        'page_obj': page_obj,
    }
    return render(request, 'Food/index.html', context)

class IndexClassView(ListView):
    model = Item
    template_name = 'Food/index.html'
    context_object_name = 'item_list'

# def detail(request,id):
#     item = Item.objects.get(pk=id)
#     context = {
#         'item':item,
#     }
#     return render(request,'Food/detail.html',context)

class FoodDetail(DetailView):
    model = Item
    template_name = 'Food/detail.html'
    context_object_name = 'item'

def create_item(request):
    form = ItemForm(request.POST or None)
    if request.method=="POST":
        if form.is_valid():
            form.save()
            return redirect("Food:index")
        
    context = {
        'form' : form,
    }
    return render(request,'food/item-form.html',context)

# class ItemCreateView(CreateView):
#     model = Item
#     fields = ['item_name','item_desc','item_price','item_image']
    
#     def form_valid(self,form):
#         form.instance.user_name = self.request.user
#         return super().form_valid(form)

# def update_item(request,id):
#     item = Item.objects.get(id=id)
#     form = ItemForm(request.POST or None,instance=item)
    
#     if form.is_valid():
#         form.save()
#         return redirect("Food:index")
    
#     context = {
#         'form':form
#     }
    
#     return render(request, 'Food/item-form.html',context)

class ItemUpdateView(UpdateView):
    model = Item
    fields = ['item_name','item_desc','item_price','item_image']
    template_name_suffix = '_update_form'
    
    def get_queryset(self):
        return Item.objects.filter(user_name=self.request.user)

def delete_item(request,id):
    item = Item.objects.get(id=id)
    if request.method=='POST':
        item.delete()
        return redirect('Food:index')
    
    return render(request, 'Food/item-delete.html')

class ItemDelete(DeleteView):
    model = Item
    success_url = reverse_lazy('Food:index')