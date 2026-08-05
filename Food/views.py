from decimal import Decimal

from django.contrib import messages
from django.shortcuts import get_object_or_404, render, redirect
from .models import Item,Order
from .forms import ItemForm
from django.contrib.auth.decorators import login_required
from django.views.generic.detail import DetailView
from django.views.generic.edit import UpdateView,DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.exceptions import PermissionDenied
from django.urls import reverse_lazy
from django.core.paginator import Paginator
from .serializers import ItemSerializer,OrderSerializer
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from .permissions import IsOwnerOrReadOnly, IsStaffOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter,SearchFilter
# Create your views here.

class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_staff:
            return Order.objects.all()
        return Order.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    
class ItemViewSet(viewsets.ModelViewSet):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    permission_classes = [IsStaffOrReadOnly, IsOwnerOrReadOnly]
    filter_backends = [DjangoFilterBackend,OrderingFilter,SearchFilter]
    filterset_fields = ["item_name","item_price"]
    ordering_fields = ["item_name","item_price"]
    search_fields = ["item_name","item_desc","item_price"]
    
    def perform_create(self, serializer):
        serializer.save(user_name=self.request.user)
    
@login_required
def index(request):
    item_list = Item.objects.all()
    paginator = Paginator(item_list,6)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    context = {
        'page_obj': page_obj,
    }
    return render(request, 'Food/index.html', context)

class FoodDetail(DetailView):
    model = Item
    template_name = 'Food/detail.html'
    context_object_name = 'item'

@login_required
def create_item(request):
    if not request.user.is_staff:
        raise PermissionDenied

    form = ItemForm(request.POST or None, request.FILES or None)
    if request.method=="POST":
        if form.is_valid():
            item = form.save(commit=False)
            item.user_name = request.user
            item.save()
            return redirect("Food:index")
        
    context = {
        'form' : form,
    }
    return render(request, 'Food/item_form.html', context)


def _cart_item_ids(request):
    return request.session.get("cart_item_ids", [])


@login_required
def add_to_cart(request, pk):
    if request.method != "POST":
        return redirect("Food:detail", pk=pk)

    item = get_object_or_404(Item, pk=pk, is_available=True)
    cart_item_ids = _cart_item_ids(request)
    item_id = str(item.pk)
    if item_id not in cart_item_ids:
        cart_item_ids.append(item_id)
        request.session["cart_item_ids"] = cart_item_ids
        messages.success(request, f"{item.item_name} was added to your cart.")
    else:
        messages.info(request, f"{item.item_name} is already in your cart.")
    return redirect("Food:cart")


@login_required
def cart(request):
    cart_item_ids = _cart_item_ids(request)
    cart_items = list(Item.objects.filter(pk__in=cart_item_ids, is_available=True))
    available_ids = {str(item.pk) for item in cart_items}
    if available_ids != set(cart_item_ids):
        request.session["cart_item_ids"] = [
            item_id for item_id in cart_item_ids if item_id in available_ids
        ]

    return render(
        request,
        "Food/cart.html",
        {
            "cart_items": cart_items,
            "total": sum((item.item_price for item in cart_items), Decimal("0.00")),
        },
    )


@login_required
def remove_from_cart(request, pk):
    if request.method == "POST":
        cart_item_ids = _cart_item_ids(request)
        item_id = str(pk)
        request.session["cart_item_ids"] = [
            existing_id for existing_id in cart_item_ids if existing_id != item_id
        ]
        messages.success(request, "Item removed from your cart.")
    return redirect("Food:cart")


@login_required
def checkout(request):
    if request.method != "POST":
        return redirect("Food:cart")

    cart_item_ids = _cart_item_ids(request)
    cart_items = list(Item.objects.filter(pk__in=cart_item_ids, is_available=True))
    if not cart_items:
        messages.error(request, "Your cart is empty or its items are no longer available.")
        return redirect("Food:cart")

    order = Order.objects.create(user=request.user)
    order.item.set(cart_items)
    request.session["cart_item_ids"] = []
    messages.success(request, "Your order has been placed successfully.")
    return redirect("Food:order_history")


@login_required
def order_history(request):
    orders = Order.objects.filter(user=request.user).prefetch_related("item").order_by("-ordered_at")
    return render(request, "Food/order_history.html", {"orders": orders})

class StaffRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    raise_exception = True

    def test_func(self):
        return self.request.user.is_staff


class ItemUpdateView(StaffRequiredMixin, UpdateView):
    model = Item
    form_class = ItemForm
    template_name_suffix = '_update_form'
    
    def get_queryset(self):
        return Item.objects.filter(user_name=self.request.user)

class ItemDelete(StaffRequiredMixin, DeleteView):
    model = Item
    success_url = reverse_lazy('Food:index')

    def get_queryset(self):
        return Item.objects.filter(user_name=self.request.user)
