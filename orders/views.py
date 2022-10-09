from django.shortcuts import render, redirect, Http404
from django.views import generic
from orders.forms import OrderForm
from orders.models import Order, OrderItem
from cart.cart import Cart
from django.db.models import Count
from course.models import Course
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
# Create your views here.


class CreateOrder(LoginRequiredMixin, generic.CreateView):
    template_name = 'orders/place_order.html'
    form_class = OrderForm
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart = Cart(self.request)
        courses = Course.objects.filter(pk__in=cart.cart.keys())
        cart_items = map(
            lambda p: {'course': p,'total': p.price}, courses)
        context['summary'] = cart_items
        return context

    def form_valid(self, form):
        cart = Cart(self.request)
        order = form.save(commit=False)
        order.user = self.request.user
        order.total_price = cart.get_total_price()
        order.save()
        courses = Course.objects.filter(id__in=cart.cart.keys())
        orderitems = []
        for i in courses:
            orderitems.append(OrderItem(order=order, course=i, total=i.price))
        OrderItem.objects.bulk_create(orderitems)
        cart.clear()
        messages.success(self.request, 'Đặt hàng thành công.')
        return redirect('course:courselist')


class MyOrders(LoginRequiredMixin, generic.ListView):
    model = Course,Order, OrderItem
    template_name = 'orders/order_list.html'
    context_object_name = 'course_list'
    paginate_by = 20

    def get_queryset(self):
        orders = Order.objects.filter(user=self.request.user)
        course_list = []
        for order in orders:
            for course_item in OrderItem.objects.filter(order_id=order.id):
                    course_list.append(Course.objects.filter(id=course_item.course_id))
        return course_list


class OrderDetails(LoginRequiredMixin, generic.DetailView):
    model = Order
    context_object_name = 'order'
    template_name = 'orders/order_details.html'

    def get_queryset(self, **kwargs):
        objs = super().get_queryset(**kwargs)
        return objs.filter(user=self.request.user).prefetch_related('items', 'items__product')


class OrderInvoice(LoginRequiredMixin, generic.DetailView):
    model = Order
    context_object_name = 'order'
    template_name = 'orders/order_invoice.html'

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.prefetch_related('items', 'items__product')

    def get_object(self, **kwargs):
        obj = super().get_object(**kwargs)
        if obj.user_id == self.request.user.id or self.request.user.is_superuser:
            return obj
        raise Http404
