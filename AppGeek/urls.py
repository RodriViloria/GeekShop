from django.shortcuts import redirect
from django.urls import path, include
from .views import index, categorias, productos, clientes, buscar_producto,about,crear_producto,save_comment,crear_reporte,ProductoDetalleView,EditarProductoView,TrekkingView, TrekkingDetailView
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('index/', index, name='index'),
    path('categoria/', categorias, name='categoria'),
    path('producto/', productos, name='producto'),
    path('cliente/', clientes, name='cliente'),
    path('buscar_producto/', buscar_producto, name='buscar_producto'),
    path('', lambda request: redirect('index/'), name='inicio'),
     path('crear_producto/', crear_producto, name='crear_producto'),
    path('about/', about, name='about'),
    path('home/', include('accounts.urls')),
    path('producto/<int:pk>', ProductoDetalleView.as_view(), name="ProductoDetail"),
    path('editar_producto/<int:pk>', EditarProductoView.as_view(), name='editar_producto'),
    path('trekking/', TrekkingView.as_view(), name='trekking_list'),
    path('trekking/<int:trekking_id>/', TrekkingDetailView.as_view(), name='trekking_detail'),
    path('trekking/<int:trekking_id>/save_comment/', save_comment, name='save_comment'),
    path('crear-reporte/', crear_reporte, name='crear_reporte'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)