from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect
from django.utils.decorators import method_decorator
from django.views import View
from .models import Trekking, Comments, Producto, Cliente, Categoria, Trekking
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import CategoriaForm, ProductoForm, ClienteForm, BusquedaForm, CommentForm, TrekkingForm
from django.contrib.auth.decorators import login_required


# pylint: disable=no-member


def crear_producto(request):
    if request.method == 'POST':
        form = ProductoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('producto')
    else:
        form = ProductoForm()

    return render(request, 'producto.html', {'form': form})


@login_required(login_url='login')
def index(request):
    # Imprimir en la consola si el usuario está autenticado
    if request.user.is_authenticated:
        print(f"El usuario {request.user} está autenticado.")
    else:
        print("El usuario no está autenticado.")

    return render(request, 'index.html')


@login_required(login_url='login')
def categorias(request):
    # Obtener todas las categorías
    categorias = Categoria.objects.all()

    if request.method == 'POST':
        form = CategoriaForm(request.POST)
        if form.is_valid():
            categoria = form.save()
            return redirect('index')
    else:
        form = CategoriaForm()

    # Pasar la lista de categorías al contexto
    return render(request, 'categoria.html', {'form': form, 'categorias': categorias})


@login_required(login_url='login')
def productos(request):
    productos = Producto.objects.all()
    if request.method == 'POST':
        nombre = request.POST.get('eliminarProducto')
        if nombre:
            producto = Producto.objects.filter(nombre=nombre).first()
            if producto:
                producto.delete()
                print("Producto eliminado:", nombre)
                return redirect('producto')

    form = ProductoForm()
    return render(request, 'producto.html', {'productos': productos, 'form': form})


@login_required(login_url='login')
def clientes(request):
    # Obtener todos los clientes
    clientes = Cliente.objects.all()

    if request.method == 'POST':
        form = ClienteForm(request.POST)
        if form.is_valid():
            cliente = form.save()
            return redirect('index')
    else:
        form = ClienteForm()

    # Pasar la lista de clientes al contexto
    return render(request, 'cliente.html', {'form': form, 'clientes': clientes})


@login_required(login_url='login')
def buscar_producto(request):
    form = BusquedaForm(request.GET or None)
    resultados = Producto.objects.all()

    if form.is_valid():
        query = form.cleaned_data['query']
        resultados = Producto.objects.filter(nombre__icontains=query)

    return render(request, 'buscar_producto.html', {'form': form, 'resultados': resultados})


class EditarProductoView(LoginRequiredMixin, View):
    template_name = 'editar_producto.html'  # Ajusta según tu estructura de carpetas

    def get(self, request, pk):
        producto = get_object_or_404(Producto, pk=pk)
        form = ProductoForm(instance=producto)
        return render(request, self.template_name, {'form': form, 'producto': producto})

    def post(self, request, pk):
        producto = get_object_or_404(Producto, pk=pk)
        form = ProductoForm(request.POST, request.FILES, instance=producto)

        if form.is_valid():
            form.save()
            return redirect('ProductoDetalle', pk=pk)  # Redirige a la vista de detalle después de la edición

        return render(request, self.template_name, {'form': form, 'producto': producto})


class ProductoDetalleView(LoginRequiredMixin, View):
    template_name = 'productodetalle.html'

    def get(self, request, pk):
        # Obtener el objeto producto por su clave primaria (pk)
        producto = Producto.objects.get(pk=pk)

        # Renderizar la plantilla con el objeto producto en el contexto
        return render(request, self.template_name, {'producto': producto})


# Error 404 / 500


def pagina_no_encontrada(request):
    return render(request, '404.html')


def error_servidor(request):
    return render(request, '500.html', status=500)


def about(request):
    return render(request, 'about.html')


@login_required
def crear_reporte(request):
    if request.method == 'POST':
        form = TrekkingForm(request.POST)
        if form.is_valid():
            reporte = form.save(commit=False)

            # Asociar el usuario logueado al objeto Trekking
            reporte.usuario = request.user

            # Puedes configurar el trekking directamente si está disponible en tu lógica
            # reporte.trekking = tu_trekking

            reporte.save()
            return redirect('detalle_trekking',
                            trekking_id=reporte.id)  # Usar reporte.id en lugar de reporte.trekking.id

    else:
        form = TrekkingForm()

    return render(request, 'partials/crear_reporte.html', {'form': form})


class TrekkingView(LoginRequiredMixin, View):
    template_name = 'trekking_list.html'

    @method_decorator(login_required(login_url='login'))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        trekking_list = Trekking.objects.all()

        trekking_abierto = trekking_list.filter(estado='Abierto')
        trekking_en_progreso = trekking_list.filter(estado='En Curso')
        trekking_cerrado = trekking_list.filter(estado='Cerrado')

        return render(request, self.template_name, {
            'trekking_abierto': trekking_abierto,
            'trekking_en_progreso': trekking_en_progreso,
            'trekking_cerrado': trekking_cerrado,
            'comment_form': CommentForm
        })

    def post(self, request, *args, **kwargs):
        comment_form = CommentForm(request.POST)

        if comment_form.is_valid():
            trekking_id = comment_form.cleaned_data['trekking_id']
            trekking_instance = get_object_or_404(Trekking, id=trekking_id)

            # Procesa el formulario y guarda el comentario, ajusta según sea necesario
            new_comment = comment_form.save(commit=False)
            new_comment.user = request.user
            new_comment.trekking = trekking_instance
            new_comment.save()

            return redirect('trekking_list')

        # If the form is not valid, re-render the page with the form and existing data
        trekking_abierto, trekking_en_progreso, trekking_cerrado = self.get_trekking_lists()

        return render(request, self.template_name, {
            'trekking_abierto': trekking_abierto,
            'trekking_en_progreso': trekking_en_progreso,
            'trekking_cerrado': trekking_cerrado,
            'comment_form': comment_form,
        })


class TrekkingDetailView(View):
    template_name = 'trekking_detail.html'

    @method_decorator(login_required(login_url='login'))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, trekking_id, *args, **kwargs):
        trekking = get_object_or_404(Trekking, id=trekking_id)
        form = CommentForm(trekking, initial={'trekking': trekking})
        comments = trekking.comments.all()
        return render(request, self.template_name, {'trekking': trekking, 'comments': comments, 'form': form})

    def post(self, request, trekking_id, *args, **kwargs):
        trekking = get_object_or_404(Trekking, id=trekking_id)

        # Si hay un comentario a eliminar
        if 'delete_comment' in request.POST:
            comment_id_to_delete = request.POST.get('delete_comment')
            comment_to_delete = get_object_or_404(Comments, id=comment_id_to_delete, usuario=request.user)
            comment_to_delete.delete()

            # Inicializa el formulario con datos predeterminados antes de renderizar la vista
            form = CommentForm(trekking, initial={'trekking': trekking})
            comments = trekking.comments.all()
            return render(request, self.template_name, {'trekking': trekking, 'comments': comments, 'form': form})

        # Resto del código para agregar comentarios, actualizar estado, etc.
        form = CommentForm(trekking, request.POST, request.FILES, initial={'trekking': trekking})

        if form.is_valid():
            save_comment = form.save(commit=False)
            save_comment.usuario = request.user
            save_comment.trekking = trekking
            save_comment.save()

            # Actualizar el estado en el modelo Comments
            trekking.estado = form.cleaned_data['estado']
            trekking.save()

            # Redirige a la lista de trekking después de guardar un comentario
            return redirect('trekking_list')

        else:
            comments = trekking.comments.all()
            return render(request, self.template_name, {'trekking': trekking, 'comments': comments, 'form': form})


@login_required(login_url='login')
def save_comment(request, trekking_id):
    trekking = get_object_or_404(Trekking, id=trekking_id)

    if request.method == "POST":
        form = CommentForm(trekking, request.POST)  # Pasa el objeto 'trekking' al instanciar el formulario
        if form.is_valid():
            save_comment = form.save(commit=False)
            save_comment.usuario = request.user
            save_comment.trekking = trekking
            save_comment.save()

            return redirect('trekking_detail', trekking_id=trekking.id)
    else:
        form = CommentForm(trekking)  # También pasa 'trekking' cuando el método no es POST

    return render(request, 'comment_form.html', {'form': form, 'trekking': trekking})
