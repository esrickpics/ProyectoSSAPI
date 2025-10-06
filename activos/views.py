from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView
)
from django.contrib import messages
from django.db.models import Q
from .models import Categoria, SubCategoria, Ubicacion, Activo, HistorialMovimiento
from .forms import (
    CategoriaForm, SubCategoriaForm, UbicacionForm, 
    ActivoForm, ActivoFilterForm, ReasignarActivoForm, ReubicarActivoForm
)


# ============== VISTAS DE CATEGORÍA ==============

class CategoriaListView(ListView):
    model = Categoria
    template_name = 'activos/categoria_list.html'
    context_object_name = 'categorias'
    paginate_by = 20


class CategoriaCreateView(CreateView):
    model = Categoria
    form_class = CategoriaForm
    template_name = 'activos/categoria_form.html'
    success_url = reverse_lazy('activos:categoria-list')
    
    def form_valid(self, form):
        messages.success(self.request, 'Categoría creada exitosamente.')
        return super().form_valid(form)


class CategoriaUpdateView(UpdateView):
    model = Categoria
    form_class = CategoriaForm
    template_name = 'activos/categoria_form.html'
    success_url = reverse_lazy('activos:categoria-list')
    
    def form_valid(self, form):
        messages.success(self.request, 'Categoría actualizada exitosamente.')
        return super().form_valid(form)


class CategoriaDeleteView(DeleteView):
    model = Categoria
    template_name = 'activos/categoria_confirm_delete.html'
    success_url = reverse_lazy('activos:categoria-list')
    
    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        
        # Verificar si tiene subcategorías asociadas
        if self.object.subcategorias.exists():
            messages.error(self.request, f'No se puede eliminar la categoría "{self.object.nombre}" porque tiene subcategorías asociadas.')
            return redirect('activos:categoria-list')
        
        messages.success(self.request, 'Categoría eliminada exitosamente.')
        return super().delete(request, *args, **kwargs)


# ============== VISTAS DE SUBCATEGORÍA ==============

class SubCategoriaListView(ListView):
    model = SubCategoria
    template_name = 'activos/subcategoria_list.html'
    context_object_name = 'subcategorias'
    paginate_by = 20
    
    def get_queryset(self):
        queryset = super().get_queryset().select_related('categoria')
        categoria_id = self.request.GET.get('categoria')
        if categoria_id:
            queryset = queryset.filter(categoria_id=categoria_id)
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categorias'] = Categoria.objects.all()
        return context


class SubCategoriaCreateView(CreateView):
    model = SubCategoria
    form_class = SubCategoriaForm
    template_name = 'activos/subcategoria_form.html'
    success_url = reverse_lazy('activos:subcategoria-list')
    
    def form_valid(self, form):
        messages.success(self.request, 'Subcategoría creada exitosamente.')
        return super().form_valid(form)


class SubCategoriaUpdateView(UpdateView):
    model = SubCategoria
    form_class = SubCategoriaForm
    template_name = 'activos/subcategoria_form.html'
    success_url = reverse_lazy('activos:subcategoria-list')
    
    def form_valid(self, form):
        messages.success(self.request, 'Subcategoría actualizada exitosamente.')
        return super().form_valid(form)


class SubCategoriaDeleteView(DeleteView):
    model = SubCategoria
    template_name = 'activos/subcategoria_confirm_delete.html'
    success_url = reverse_lazy('activos:subcategoria-list')
    
    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        
        # Verificar si tiene activos asociados
        if self.object.activos.exists():
            messages.error(self.request, f'No se puede eliminar la subcategoría "{self.object}" porque tiene activos asociados.')
            return redirect('activos:subcategoria-list')
        
        messages.success(self.request, 'Subcategoría eliminada exitosamente.')
        return super().delete(request, *args, **kwargs)


# ============== VISTAS DE UBICACIÓN ==============

class UbicacionListView(ListView):
    model = Ubicacion
    template_name = 'activos/ubicacion_list.html'
    context_object_name = 'ubicaciones'
    paginate_by = 20


class UbicacionCreateView(CreateView):
    model = Ubicacion
    form_class = UbicacionForm
    template_name = 'activos/ubicacion_form.html'
    success_url = reverse_lazy('activos:ubicacion-list')
    
    def form_valid(self, form):
        messages.success(self.request, 'Ubicación creada exitosamente.')
        return super().form_valid(form)


class UbicacionUpdateView(UpdateView):
    model = Ubicacion
    form_class = UbicacionForm
    template_name = 'activos/ubicacion_form.html'
    success_url = reverse_lazy('activos:ubicacion-list')
    
    def form_valid(self, form):
        messages.success(self.request, 'Ubicación actualizada exitosamente.')
        return super().form_valid(form)


class UbicacionDeleteView(DeleteView):
    model = Ubicacion
    template_name = 'activos/ubicacion_confirm_delete.html'
    success_url = reverse_lazy('activos:ubicacion-list')
    
    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        
        # Verificar si tiene activos asociados
        if self.object.activos.exists():
            messages.error(self.request, f'No se puede eliminar la ubicación "{self.object.nombre}" porque tiene activos asociados.')
            return redirect('activos:ubicacion-list')
        
        messages.success(self.request, 'Ubicación eliminada exitosamente.')
        return super().delete(request, *args, **kwargs)


# ============== VISTAS DE ACTIVO ==============

class ActivoListView(ListView):
    model = Activo
    template_name = 'activos/activo_list.html'
    context_object_name = 'activos'
    paginate_by = 25
    
    def get_queryset(self):
        queryset = super().get_queryset().select_related(
            'subcategoria__categoria', 'ubicacion', 'usuario_asignado'
        )
        
        # Filtros
        categoria_id = self.request.GET.get('categoria')
        subcategoria_id = self.request.GET.get('subcategoria')
        ubicacion_id = self.request.GET.get('ubicacion')
        estado = self.request.GET.get('estado')
        buscar = self.request.GET.get('buscar')
        
        if categoria_id:
            queryset = queryset.filter(subcategoria__categoria_id=categoria_id)
        if subcategoria_id:
            queryset = queryset.filter(subcategoria_id=subcategoria_id)
        if ubicacion_id:
            queryset = queryset.filter(ubicacion_id=ubicacion_id)
        if estado:
            queryset = queryset.filter(estado=estado)
        if buscar:
            queryset = queryset.filter(
                Q(codigo_inventario__icontains=buscar) |
                Q(marca__icontains=buscar) |
                Q(modelo__icontains=buscar) |
                Q(numero_serial__icontains=buscar)
            )
        
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter_form'] = ActivoFilterForm(self.request.GET or None)
        context['total_activos'] = self.get_queryset().count()
        
        # Estadísticas para el dashboard
        from django.db.models import Count
        from .models import Categoria, Ubicacion
        
        # Total de activos por categoría
        context['activos_por_categoria'] = Categoria.objects.annotate(
            total_activos=Count('subcategorias__activos')
        ).order_by('-total_activos')
        
        # Total de activos por ubicación
        context['activos_por_ubicacion'] = Ubicacion.objects.annotate(
            total_activos=Count('activos')
        ).order_by('-total_activos')
        
        # Estadísticas generales
        context['total_categorias'] = Categoria.objects.count()
        context['total_ubicaciones'] = Ubicacion.objects.count()
        context['total_activos_sistema'] = Activo.objects.count()
        
        return context


class ActivoDetailView(DetailView):
    model = Activo
    template_name = 'activos/activo_detail.html'
    context_object_name = 'activo'
    
    def get_queryset(self):
        return super().get_queryset().select_related(
            'subcategoria__categoria', 'ubicacion', 'usuario_asignado'
        )


class ActivoCreateView(CreateView):
    model = Activo
    form_class = ActivoForm
    template_name = 'activos/activo_form.html'
    success_url = reverse_lazy('activos:activo-list')
    
    def form_valid(self, form):
        messages.success(self.request, 'Activo creado exitosamente.')
        return super().form_valid(form)


class ActivoUpdateView(UpdateView):
    model = Activo
    form_class = ActivoForm
    template_name = 'activos/activo_form.html'
    success_url = reverse_lazy('activos:activo-list')
    
    def form_valid(self, form):
        messages.success(self.request, 'Activo actualizado exitosamente.')
        return super().form_valid(form)


class ActivoDeleteView(DeleteView):
    model = Activo
    template_name = 'activos/activo_confirm_delete.html'
    success_url = reverse_lazy('activos:activo-list')
    
    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Activo eliminado exitosamente.')
        return super().delete(request, *args, **kwargs)


# ============== VISTAS ESPECIALES DE ACTIVO ==============

def reasignar_activo(request, pk):
    """Vista para reasignar un activo a otro usuario"""
    activo = get_object_or_404(Activo, pk=pk)
    
    if request.method == 'POST':
        form = ReasignarActivoForm(request.POST, instance=activo)
        if form.is_valid():
            form.save()
            messages.success(request, f'Activo {activo.codigo_inventario} reasignado exitosamente.')
            return redirect('activos:activo-detail', pk=pk)
    else:
        form = ReasignarActivoForm(instance=activo)
    
    return render(request, 'activos/activo_reasignar.html', {
        'form': form,
        'activo': activo
    })


def reubicar_activo(request, pk):
    """Vista para reubicar un activo"""
    activo = get_object_or_404(Activo, pk=pk)
    
    if request.method == 'POST':
        form = ReubicarActivoForm(request.POST, instance=activo)
        if form.is_valid():
            form.save()
            messages.success(request, f'Activo {activo.codigo_inventario} reubicado exitosamente.')
            return redirect('activos:activo-detail', pk=pk)
    else:
        form = ReubicarActivoForm(instance=activo)
    
    return render(request, 'activos/activo_reubicar.html', {
        'form': form,
        'activo': activo
    })


class ActivoHistorialView(DetailView):
    """Vista para mostrar el historial de movimientos de un activo"""
    model = Activo
    template_name = 'activos/activo_historial.html'
    context_object_name = 'activo'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        activo = self.get_object()
        context['historial'] = activo.historial_movimientos.all().order_by('-fecha_movimiento')
        return context
