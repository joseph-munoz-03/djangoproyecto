import os
import django
from decimal import Decimal

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'SGIEVpy.settings')
django.setup()

from Sgiev.models import Venta, Usuarios, Producto, Venta_has_producto, Movimiento_inventario

try:
    # 🚫 Evitar duplicados
    if Venta.objects.exists():
        print("⚠️ Ya existen ventas, no se crean más")
        exit()

    usuario = Usuarios.objects.first()
    productos = list(Producto.objects.all()[:3])

    if not usuario or not productos:
        print("⚠️ No hay usuarios o productos suficientes")
        exit()

    for i in range(1, 6):  # Crear 5 ventas
        venta = Venta.objects.create(
            numero_factura=f"FAC-00{i}",
            subtotal=Decimal('100000'),
            descuento=Decimal('5000'),
            iva=Decimal('19000'),
            valor_total=Decimal('114000'),
            abono=Decimal('114000'),
            saldo_pendiente=Decimal('0'),
            estado_pago='pagado',
            metodo_pago='efectivo',
            usuarios_id_usuario=usuario,
            observaciones='Venta de prueba automática',
            imagen_recibo='recibo.jpg',
            nombre_cliente=f'Cliente {i}',
            correo_cliente=f'cliente{i}@correo.com',
            telefono_cliente='3000000000',
            direccion_cliente='Dirección prueba'
        )

        for producto in productos:
            cantidad = 2

            # 🚫 Validar stock
            if producto.stock_actual < cantidad:
                print(f"⚠️ Stock insuficiente para {producto.nombre_producto}")
                continue

            # 🧾 Crear detalle de venta
            Venta_has_producto.objects.create(
                venta_idfactura=venta,
                producto_idproducto=producto,
                cantidad=cantidad,
                valor_unitario=producto.precio_venta,
                subtotal_linea=producto.precio_venta * cantidad
            )

            # 📉 Actualizar stock
            stock_anterior = producto.stock_actual
            producto.stock_actual -= cantidad
            producto.save()

            # 📦 Movimiento de inventario
            Movimiento_inventario.objects.create(
                tipo_movimiento='venta',
                cantidad=cantidad,
                stock_anterior=stock_anterior,
                stock_nuevo=producto.stock_actual,
                precio_unitario=producto.precio_venta,
                valor_total=producto.precio_venta * cantidad,
                referencia_id=venta.id,
                tipo_referencia='venta',
                observaciones='Venta automática',
                imagen_comprobante='venta.jpg',
                usuarios_id_usuario=usuario,
                producto_idproducto=producto
            )

    print("✅ 5 ventas creadas correctamente")

except Exception as e:
    print(f"❌ Error al crear ventas: {e}")