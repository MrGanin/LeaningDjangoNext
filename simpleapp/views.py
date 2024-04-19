from datetime import datetime
from .filters import ProductFilter
from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Product
from .forms import ProductForm
from django.http import HttpResponseRedirect

class ProductsList(ListView):
    model = Product
    ordering = 'id'
    template_name = 'products.html'
    context_object_name = 'products'
    paginate_by = 1

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = ProductFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time_now'] = datetime.utcnow()
        context['next_sale'] = None
        context['filterset'] = self.filterset
        return context



class ProductDetail(DetailView):
    model = Product
    template_name = 'product.html'
    context_object_name = 'product'

def create_product(request):
    form = ProductForm()

    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/products/')


    return render(request, 'product_edit.html', {'form':form} )