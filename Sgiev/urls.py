from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('index', views.index, name='index'),
    path('login', views.login, name='login'),
    path('admin', views.admin, name='admin'),

    #CATEGORIA
    path('list_categoria/', views.list_categoria, name='list_categoria'),
    path('registro_categoria/', views.registro_categoria, name='registro_categoria'),
    path('pre_editar_categoria/<str:id>', views.pre_editar_categoria, name="pre_editar_categoria"),
    path('editar_categoria/<str:id>', views.editar_categoria, name='editar_categoria'),
    path('eliminar_categoria/<str:id>', views.eliminar_categoria, name='eliminar_categoria'),
    
    #PRODUCTO
     path('list_producto/', views.list_producto, name='list_producto'),
    path('registro_producto/', views.registro_producto, name='registro_producto'),
    path('pre_editar_producto/<str:id>', views.pre_editar_producto, name="pre_editar_producto"),
    path('editar_producto/<str:id>', views.editar_producto, name='editar_producto'),
    path('eliminar_producto/<str:id>', views.eliminar_producto, name='eliminar_producto'),
    path('inventario/salida/ajuste/', views.registrar_salida_inventario_ajuste, name='registrar_salida_inventario_ajuste'),
    path('inventario/detalle-producto/<int:producto_id>/', views.detalle_producto_modal, name='detalle_producto_modal'),
    path('producto/reporte/', views.generar_reporte_productos, name='generar_reporte_productos'),
    path('producto/editar-maestro/<int:id>/', views.editar_producto_maestro, name='editar_producto_maestro'),

    #PROVEEDOR
    path('listar_proveedores/', views.listar_proveedores, name='listar_proveedores'),
    path('proveedores/registrar/', views.registrar_proveedor, name='registrar_proveedor'),
    path('proveedores/editar/<int:id>/', views.editar_proveedor, name='editar_proveedor'),
    path('proveedores/eliminar/<int:id>/', views.eliminar_proveedor, name='eliminar_proveedor'),
    path('crear_compra_proveedor/<int:idproveedor>/', views.crear_compra_proveedor, name='crear_compra_proveedor'),
    path('compras/', views.listar_compras_proveedor, name='listar_compras'),
    path('compra/detalle/<int:compra_id>/', views.detalle_compra_proveedor, name='detalle_compra'),
    path('proveedores/crear_compra/<int:idproveedor>/', views.crear_compra_proveedor, name='crear_compra_proveedor'),
    path('proveedores/quitar_producto/<int:idproveedor>/<str:temp_id>/', views.compra_quitar_producto, name='compra_quitar_producto'),
    path('proveedores/limpiar_carrito/<int:idproveedor>/', views.compra_limpiar_carrito, name='compra_limpiar_carrito'),
    path('compra/<int:compra_id>/detalle/', views.detalle_compra_proveedor, name='detalle_compra_proveedor'),
    path('compra/<int:compra_id>/recibir/', views.recibir_compra_pendiente, name='recibir_compra_pendiente'),
    path('compra/nueva/<int:idproveedor>/', views.crear_compra_proveedor, name='crear_compra_proveedor'),
    path('compra/<int:idproveedor>/quitar/<str:temp_id>/', views.compra_quitar_producto, name='compra_quitar_producto'),
    path('compra/<int:idproveedor>/limpiar/', views.compra_limpiar_carrito, name='compra_limpiar_carrito'),
    path('compra/detalle/<int:compra_id>/', views.detalle_compra_proveedor, name='detalle_compra_proveedor'),
    path('productos/por_proveedor/<int:proveedor_id>/', views.obtener_productos_por_proveedor, name='productos_por_proveedor'),
    path('proveedores/pdf/', views.proveedores_generar_pdf, name='proveedores_pdf'),


    
    
    # Autenticación
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    
    # Dashboard
    path('dashboard/', views.dashboard_view, name='dashboard'),

# CRUD Usuarios
    path('usuarios/', views.usuarios_listar, name='usuarios_listar'),
    path('usuarios/crear/', views.usuarios_crear, name='usuarios_crear'),
    path('usuarios/editar/<int:id>/', views.usuarios_editar, name='usuarios_editar'),
    path('usuarios/eliminar/<int:id>/', views.usuarios_eliminar, name='usuarios_eliminar'),
    path('usuarios/detalle/<int:id>/', views.usuarios_detalle, name='usuarios_detalle'),
    path('usuarios/perfil/', views.perfil_usuario, name='perfil_usuario'),

    
    
    
    # CRUD Ventas
    path('ventas/', views.ventas_listar, name='ventas_listar'),
    path('ventas/crear/', views.ventas_crear, name='ventas_crear'),
    path('ventas/detalle/<int:id>/', views.ventas_detalle, name='ventas_detalle'),
    path('ventas/quitar/<int:producto_id>/', views.ventas_quitar_producto, name='ventas_quitar_producto'),
    path('ventas/limpiar/', views.ventas_limpiar_carrito, name='ventas_limpiar_carrito'),
    path('ventas/editar-estado/<int:id>/', views.ventas_editar_estado, name='ventas_editar_estado'),
    path('ventas/eliminar/<int:id>/', views.ventas_eliminar, name='ventas_eliminar'),
    path('ventas/pdf/<int:id>/', views.ventas_generar_pdf, name='ventas_generar_pdf'),  
    # API para productos
    path('api/producto/<int:producto_id>/', views.obtener_precio_producto, name='obtener_precio_producto'),

 #crud mensajeria
    path('mensajeria/', views.mensajeria_listar, name='mensajeria_listar'),
    path('mensajeria/crear/', views.mensajeria_crear, name='mensajeria_crear'),
    path('mensajeria/editar/<int:id>/', views.mensajeria_editar, name='mensajeria_editar'),
    path('mensajeria/eliminar/<int:id>/', views.mensajeria_eliminar, name='mensajeria_eliminar'),
    
    # CRUD Envíos
    path('envios/', views.envios_listar, name='envios_listar'),
    path('envios/crear/', views.envios_crear, name='envios_crear'),
    path('envios/editar/<int:id>/', views.envios_editar, name='envios_editar'),
    path('envios/eliminar/<int:id>/', views.envios_eliminar, name='envios_eliminar'),
    path('envios/detalle/<int:id>/', views.envios_detalle, name='envios_detalle'),
    

]




