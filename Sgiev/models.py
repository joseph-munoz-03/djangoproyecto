from django.db import models

class Categoria(models.Model):
    nombre_categoria = models.CharField(max_length=60)
    descripcion_categoria = models.TextField()
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    activo = models.SmallIntegerField()

class Proveedor(models.Model):
    nombre_proveedor = models.CharField(max_length=100)
    correo_proveedor = models.CharField(max_length=100)
    telefono = models.CharField(max_length=20)
    direccion = models.CharField(max_length=100)
    nit = models.CharField(max_length=20)
    contacto_nombre = models.CharField(max_length=100)
    contacto_telefono = models.CharField(max_length=20)
    fecha_registro = models.DateTimeField(auto_now_add=True)
    activo = models.SmallIntegerField()

class Mensajeria(models.Model):
    nombre_mensajeria = models.CharField(max_length=45)
    tel_mensajeria = models.CharField(max_length=20)
    direccion_mensajeria = models.CharField(max_length=100)
    cobertura = models.CharField(max_length=45)
    activo = models.SmallIntegerField()

class Usuarios(models.Model):
    num_identificacion = models.BigIntegerField()
    tipo_usu = models.CharField(max_length=20)
    clave = models.CharField(max_length=128)
    p_nombre = models.CharField(max_length=15)
    s_nombre = models.CharField(max_length=15)
    p_apellido = models.CharField(max_length=15)
    s_apellido = models.CharField(max_length=15)
    correo = models.CharField(max_length=70)
    telefono = models.BigIntegerField()
    salario = models.BigIntegerField()
    fecha_nacimiento = models.DateField(null=False, blank=False)
    direccion = models.CharField(max_length=100)
    fecha_registro = models.DateTimeField(auto_now_add=True)
    activo = models.SmallIntegerField()

    # Propiedades necesarias para compatibilidad con Django auth
    @property
    def is_authenticated(self):
        """
        Siempre retorna True para usuarios autenticados
        """
        return True
    
    @property
    def is_anonymous(self):
        """
        Siempre retorna False para usuarios autenticados
        """
        return False
    
    @property
    def nombre_completo(self):
        """
        Retorna el nombre completo del usuario
        """
        return f"{self.p_nombre} {self.p_apellido}"


class Producto(models.Model):
    nombre_producto = models.CharField(max_length=100)
    descripcion_producto = models.TextField(blank=True, null=True)
    codigo_barras = models.CharField(max_length=50)
    registrosanitario = models.CharField(max_length=100)
    precio_compra = models.DecimalField(max_digits=10, decimal_places=2)
    precio_venta = models.DecimalField(max_digits=10, decimal_places=2)
    margen_ganancia = models.DecimalField(max_digits=10, decimal_places=2)
    stock_actual = models.IntegerField()
    stock_minimo = models.IntegerField()
    stock_maximo = models.IntegerField()
    fecha_vencimiento = models.DateField(null=False, blank=False)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    categoria_idcategoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    proveedor_idproveedor = models.ForeignKey(Proveedor, on_delete=models.CASCADE)
    activo = models.SmallIntegerField()
    class Meta:     
        verbose_name = "Producto"
        verbose_name_plural = "Productos"

    def __str__(self):
        
        if self.descripcion_producto:
            return f"{self.nombre_producto} - {self.descripcion_producto}"
        return self.nombre_producto

class Venta(models.Model):
    fecha_factura = models.DateTimeField(auto_now_add=True)
    numero_factura = models.CharField(max_length=50)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)
    descuento = models.DecimalField(max_digits=10, decimal_places=2)
    iva = models.DecimalField(max_digits=10, decimal_places=2)
    valor_total = models.DecimalField(max_digits=10, decimal_places=2)
    abono = models.DecimalField(max_digits=10, decimal_places=2)
    saldo_pendiente = models.DecimalField(max_digits=10, decimal_places=2)

    ESTADOS_PAGO = [
        ('pagado', 'Pagado'),
        ('pendiente', 'Pendiente'),
        ('parcial', 'Parcial'),
    ]
    estado_pago = models.CharField(max_length=20, choices=ESTADOS_PAGO, default='pagado')

    observaciones = models.TextField()

    ESTADOS_METPAGO = [
        ('efectivo', 'Efectivo'),
        ('tarjeta', 'Tarjeta'),
        ('transferencia', 'Transferencia'),
        ('mixto', 'Mixto')
    ]
    metodo_pago = models.CharField(max_length=20, choices=ESTADOS_METPAGO, default='efectivo')

    usuarios_id_usuario = models.ForeignKey(Usuarios, on_delete=models.CASCADE)
    imagen_recibo = models.CharField(max_length=255)

    # === DATOS DEL CLIENTE ===
    nombre_cliente = models.CharField(max_length=100, null=True, blank=True)
    correo_cliente = models.CharField(max_length=100, null=True, blank=True)
    telefono_cliente = models.CharField(max_length=20, null=True, blank=True)
    direccion_cliente = models.CharField(max_length=150, null=True, blank=True)


class Envio(models.Model):
    estado_envio = models.CharField(max_length=15)
    fecha_envio = models.DateField(null=False, blank=False)
    fecha_entrega = models.DateField(null=False, blank=False)
    direccion_envio = models.CharField(max_length=100)
    direccion_salida = models.CharField(max_length=100)
    observaciones = models.TextField()
    novedades = models.TextField()
    fk_mensajeria = models.ForeignKey(Mensajeria, on_delete=models.CASCADE)
    usuarios_id_usuario = models.ForeignKey(Usuarios, on_delete=models.CASCADE)
    venta_idfactura = models.ForeignKey(Venta, on_delete=models.CASCADE)

class Movimiento_inventario(models.Model):
     fecha_movimiento = models.DateTimeField(auto_now_add=True)
     TIPO_MOV = [
          ('entrada', 'Entrada'),
          ('salida', 'Salida'),
          ('ajuste', 'Ajuste'),
          ('venta', 'Venta'),
          ('compra', 'Compra')
     ]
     tipo_movimiento = models.CharField(max_length=20, choices=TIPO_MOV)
     cantidad = models.IntegerField()
     stock_anterior = models.IntegerField()
     stock_nuevo = models.IntegerField()
     precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)
     valor_total = models.DecimalField(max_digits=10, decimal_places=2)
     referencia_id = models.IntegerField()
     TIPO_REF = [
          ('venta', 'Venta'),
          ('compra', 'compra'),
          ('ajuste', 'Ajuste')
     ]
     tipo_referencia = models.CharField(max_length=20, choices=TIPO_REF)
     observaciones = models.TextField()
     imagen_comprobante = models.CharField(max_length=250)
     usuarios_id_usuario = models.ForeignKey(Usuarios, on_delete=models.CASCADE)
     producto_idproducto = models.ForeignKey(Producto, on_delete=models.CASCADE)

class Compra_proveedor(models.Model):
     fecha_compra = models.DateTimeField(auto_now_add=True)
     numero_factura_compra = models.CharField(max_length=10)
     subtotal_compra = models.DecimalField(max_digits=10, decimal_places=2)
     iva_compra = models.DecimalField(max_digits=10, decimal_places=2)
     total_compra = models.DecimalField(max_digits=10, decimal_places=2)
     ESTADO_COMP = [
          ('pendiente', 'pendiente'),
          ('recibida', 'recibida'),
          ('cancelada', 'Cancelada')
     ]
     estado_compra = models.CharField(max_length=20, choices=ESTADO_COMP)
     observaciones_compra = models.TextField()
     imagen_factura_compra = models.CharField(max_length=255)
     usuarios_id_usuario = models.ForeignKey(Usuarios, on_delete=models.CASCADE)
     proveedor_idproveedor = models.ForeignKey(Proveedor, on_delete=models.CASCADE)

class Compra_detalle(models.Model):
     compra_idcompra = models.ForeignKey(Compra_proveedor, on_delete=models.CASCADE)
     producto_idproducto = models.ForeignKey(Producto, on_delete=models.CASCADE)
     cantidad = models.IntegerField()
     precio_compra_unitario = models.DecimalField(max_digits=10, decimal_places=2)
     subtotal_linea_compra = models.DecimalField(max_digits=10, decimal_places=2)
     lote = models.CharField(max_length=50)
     fecha_vencimiento = models.DateField(null=False, blank=False)

class Venta_has_producto(models.Model):
     venta_idfactura = models.ForeignKey(Venta, on_delete=models.CASCADE)
     producto_idproducto = models.ForeignKey(Producto, on_delete=models.CASCADE)
     cantidad = models.IntegerField()
     valor_unitario = models.DecimalField(max_digits=10, decimal_places=2)
     subtotal_linea = models.DecimalField(max_digits=10, decimal_places=2) 