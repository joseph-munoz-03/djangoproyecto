from django import forms
from django.contrib.auth.hashers import make_password, check_password
from .models import Usuarios, Venta, Producto, Venta_has_producto, Envio, Mensajeria, Proveedor
from decimal import Decimal
from django.db.models import Sum
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from datetime import date
from dateutil.relativedelta import relativedelta
import re
#------------envios
class EnvioEditarOperarioForm(forms.ModelForm):
    """
    Formulario limitado para que operarios solo editen el estado
    """
    ESTADOS_ENVIO = [
        ('pendiente', 'Pendiente'),
        ('en_transito', 'En Tránsito'),
        ('entregado', 'Entregado'),
        ('devuelto', 'Devuelto')
    ]
    
    estado_envio = forms.ChoiceField(
        choices=ESTADOS_ENVIO,
        widget=forms.Select(attrs={'class': 'form-control', 'required': 'required'}),
        label='Estado del Envío'
    )
    
    # Campo para novedades (opcional para operarios)
    novedades = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'placeholder': 'Registre aquí cualquier novedad del envío',
            'rows': 4
        }),
        label='Novedades'
    )
    
    class Meta:
        model = Envio
        fields = ['estado_envio', 'novedades']

    
    # Campo para novedades (opcional para operarios)
    novedades = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'placeholder': 'Registre aquí cualquier novedad del envío',
            'rows': 4
        }),
        label='Novedades'
    )
    
    class Meta:
        model = Envio
        fields = ['estado_envio', 'novedades']


# ===== FORMULARIOS DE MENSAJERÍA =====

class MensajeriaForm(forms.ModelForm):
    """
    Formulario para gestionar empresas de mensajería
    """
    class Meta:
        model = Mensajeria
        fields = ['nombre_mensajeria', 'tel_mensajeria', 'direccion_mensajeria', 'cobertura', 'activo']
        
        widgets = {
            'nombre_mensajeria': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombre de la empresa',
                'required': 'required'
            }),
            'tel_mensajeria': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Teléfono de contacto',
                'required': 'required'
            }),
            'direccion_mensajeria': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Dirección de la empresa',
                'required': 'required'
            }),
            'cobertura': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: Nacional, Bogotá, Regional',
                'required': 'required'
            }),
            'activo': forms.Select(attrs={
                'class': 'form-control',
                'required': 'required'
            }, choices=[(1, 'Activo'), (0, 'Inactivo')])
        }
        
        labels = {
            'nombre_mensajeria': 'Nombre de la Empresa',
            'tel_mensajeria': 'Teléfono',
            'direccion_mensajeria': 'Dirección',
            'cobertura': 'Cobertura',
            'activo': 'Estado'
        }


# ===== FORMULARIOS DE ENVÍOS =====

class EnvioForm(forms.ModelForm):
    """
    Formulario para registrar envíos
    """
    ESTADOS_ENVIO = [
        ('pendiente', 'Pendiente'),
        ('en_transito', 'En Tránsito'),
        ('entregado', 'Entregado'),
        ('devuelto', 'Devuelto')
    ]
    
    estado_envio = forms.ChoiceField(
        choices=ESTADOS_ENVIO,
        widget=forms.Select(attrs={'class': 'form-control', 'required': 'required'}),
        label='Estado del Envío'
    )
    
    class Meta:
        model = Envio
        fields = [
            'venta_idfactura',
            'fk_mensajeria',
            'estado_envio',
            'fecha_envio',
            'fecha_entrega',
            'direccion_salida',
            'direccion_envio',
            'observaciones',
            'novedades'
        ]
        
        widgets = {
            'venta_idfactura': forms.Select(attrs={
                'class': 'form-control select2',
                'required': 'required'
            }),
            'fk_mensajeria': forms.Select(attrs={
                'class': 'form-control select2',
                'required': 'required'
            }),
            'fecha_envio': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date',
                'required': 'required'
            }, format='%Y-%m-%d'),  # Formato ISO
            'fecha_entrega': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date',
                'required': 'required'
            }, format='%Y-%m-%d'),  # Formato ISO
            'direccion_salida': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Dirección de origen',
                'required': 'required'
            }),
            'direccion_envio': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Dirección de destino',
                'required': 'required'
            }),
            'observaciones': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Observaciones adicionales',
                'rows': 3
            }),
            'novedades': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Novedades del envío',
                'rows': 3
            })
        }
        
        labels = {
            'venta_idfactura': 'Factura de Venta',
            'fk_mensajeria': 'Empresa de Mensajería',
            'fecha_envio': 'Fecha de Envío',
            'fecha_entrega': 'Fecha de Entrega Estimada',
            'direccion_salida': 'Dirección de Salida',
            'direccion_envio': 'Dirección de Envío',
            'observaciones': 'Observaciones',
            'novedades': 'Novedades'
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Si estamos editando, permitir la venta actual
        if self.instance and self.instance.pk:
            ventas_disponibles = Venta.objects.all().order_by('-fecha_factura')
        else:
            # Al crear, solo mostrar ventas SIN envío asociado
            ventas_con_envio = Envio.objects.values_list('venta_idfactura', flat=True)
            ventas_disponibles = Venta.objects.exclude(id__in=ventas_con_envio).order_by('-fecha_factura')
        
        self.fields['venta_idfactura'].queryset = ventas_disponibles
        self.fields['fk_mensajeria'].queryset = Mensajeria.objects.filter(activo=1)
        
        # Personalizar display
        self.fields['venta_idfactura'].label_from_instance = lambda obj: f"{obj.numero_factura} - ${obj.valor_total:,.0f} - {obj.usuarios_id_usuario.nombre_completo}"
        self.fields['fk_mensajeria'].label_from_instance = lambda obj: f"{obj.nombre_mensajeria} - {obj.cobertura}"
        
        # IMPORTANTE: Convertir fechas al formato correcto para el widget
        if self.instance and self.instance.pk:
            if self.instance.fecha_envio:
                self.initial['fecha_envio'] = self.instance.fecha_envio.strftime('%Y-%m-%d')
            if self.instance.fecha_entrega:
                self.initial['fecha_entrega'] = self.instance.fecha_entrega.strftime('%Y-%m-%d')
    
    def clean_venta_idfactura(self):
        """
        Valida que la venta no tenga ya un envío asociado (excepto al editar)
        """
        venta = self.cleaned_data.get('venta_idfactura')
        
        if self.instance and self.instance.pk:
            envio_existente = Envio.objects.filter(venta_idfactura=venta).exclude(pk=self.instance.pk).exists()
        else:
            envio_existente = Envio.objects.filter(venta_idfactura=venta).exists()
        
        if envio_existente:
            raise forms.ValidationError(
                f'La venta {venta.numero_factura} ya tiene un envío asociado. '
                'Cada venta solo puede tener un envío.'
            )
        
        return venta


#form de las ventas 
from django import forms
from django.db.models import Sum
from django.contrib.auth.hashers import check_password

from .models import Venta, Producto, Usuarios


class EditarEstadoVentaForm(forms.ModelForm):
    nuevo_abono = forms.DecimalField(
        max_digits=10,
        decimal_places=2,
        required=False,
        initial=0,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': '0.00',
            'step': '0.01',
            'min': '0'
        }),
        label='Nuevo Abono',
        help_text='Ingrese el valor adicional a abonar'
    )
    
    class Meta:
        model = Venta
        fields = [
            'nombre_cliente',
            'correo_cliente',
            'telefono_cliente',
            'direccion_cliente',
            'observaciones'
        ]
        widgets = {
            'nombre_cliente': forms.TextInput(attrs={'class': 'form-control'}),
            'correo_cliente': forms.EmailInput(attrs={'class': 'form-control'}),
            'telefono_cliente': forms.TextInput(attrs={'class': 'form-control'}),
            'direccion_cliente': forms.TextInput(attrs={'class': 'form-control'}),
            'observaciones': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
    
    def __init__(self, *args, **kwargs):
        self.venta = kwargs.pop('venta', None)
        super().__init__(*args, **kwargs)
        
        # Si la venta ya está pagada, deshabilitar el campo de abono
        if self.venta and self.venta.estado_pago == 'pagado':
            self.fields['nuevo_abono'].disabled = True
            self.fields['nuevo_abono'].help_text = 'La venta ya está completamente pagada'
    
    def clean_nuevo_abono(self):
        nuevo_abono = self.cleaned_data.get('nuevo_abono') or Decimal('0')
        
        if nuevo_abono < 0:
            raise ValidationError('El abono no puede ser negativo')
        
        if self.venta and nuevo_abono > 0:
            # Validar que no exceda el saldo pendiente
            if nuevo_abono > self.venta.saldo_pendiente:
                raise ValidationError(
                    f'El abono no puede ser mayor al saldo pendiente (${self.venta.saldo_pendiente:,.0f})'
                )
        
        return nuevo_abono


class VentaForm(forms.ModelForm):
    """
    Formulario para registrar ventas con validación de abono
    e información del cliente.
    """
    class Meta:
        model = Venta
        fields = [
            'numero_factura',
            'descuento',
            'metodo_pago',
            'estado_pago',
            'abono',
            'observaciones',
            'nombre_cliente',
            'correo_cliente',
            'telefono_cliente',
            'direccion_cliente',
        ]

        widgets = {
            'numero_factura': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Número de factura (ej: FAC-001)',
                'required': 'required'
            }),
            'descuento': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': '0',
                'value': '0',
                'step': '0.01',
                'min': '0',
                'id': 'id_descuento'
            }),
            'metodo_pago': forms.Select(attrs={
                'class': 'form-control',
                'required': 'required'
            }),
            'estado_pago': forms.Select(attrs={
                'class': 'form-control',
                'required': 'required',
                'id': 'id_estado_pago',
                'readonly': 'readonly'  # Se completará automáticamente en la vista
            }),
            'abono': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': '0',
                'value': '0',
                'step': '0.01',
                'min': '0',
                'id': 'id_abono'
            }),
            'observaciones': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Observaciones adicionales',
                'rows': 3
            }),
            'nombre_cliente': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombre del cliente',
                'required': 'required',
            }),
            'correo_cliente': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'correo@cliente.com',
                'required': 'required',
            }),
            'telefono_cliente': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Teléfono del cliente',
            }),
            'direccion_cliente': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Dirección del cliente',
            }),
        }

        labels = {
            'numero_factura': 'Número de Factura',
            'descuento': 'Descuento ($)',
            'metodo_pago': 'Método de Pago',
            'estado_pago': 'Estado de Pago',
            'abono': 'Abono Inicial ($)',
            'observaciones': 'Observaciones',
            'nombre_cliente': 'Nombre del Cliente',
            'correo_cliente': 'Correo del Cliente',
            'telefono_cliente': 'Teléfono del Cliente',
            'direccion_cliente': 'Dirección del Cliente',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Generar número de factura automático si es nuevo
        if not self.instance.pk:
            ultima_venta = Venta.objects.all().order_by('-id').first()
            if ultima_venta:
                try:
                    num = int(ultima_venta.numero_factura.split('-')[-1]) + 1
                    self.fields['numero_factura'].initial = f'FAC-{num:05d}'
                except Exception:
                    self.fields['numero_factura'].initial = 'FAC-00001'
            else:
                self.fields['numero_factura'].initial = 'FAC-00001'

class AgregarProductoForm(forms.Form):
    """
    Formulario para agregar productos al carrito.
    Trabaja con el producto maestro (SIN_LOTE_CATALOGO)
    y muestra el stock total sumando todos los lotes activos.
    """

    producto = forms.ModelChoiceField(
        queryset=Producto.objects.filter(
            activo=1,
            codigo_barras='SIN_LOTE_CATALOGO'  # solo maestro
        ).order_by('nombre_producto', 'descripcion_producto'),
        label='Producto',
        widget=forms.Select(attrs={
            'class': 'form-control select2-producto',
            'required': 'required',
            'id': 'id_producto'
        })
    )

    cantidad = forms.IntegerField(
        label='Cantidad',
        min_value=1,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': '1',
            'value': '1',
            'min': '1',
            'id': 'id_cantidad'
        })
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Precalcular stock total por producto maestro
        maestros = list(self.fields['producto'].queryset)
        stock_por_maestro = {}

        for maestro in maestros:
            stock_total = Producto.objects.filter(
                nombre_producto=maestro.nombre_producto,
                descripcion_producto=maestro.descripcion_producto,
                activo=1
            ).aggregate(total=Sum('stock_actual'))['total'] or 0
            stock_por_maestro[maestro.id] = stock_total

        # Guardar para usar en clean()
        self._stock_por_maestro = stock_por_maestro

        # Personalizar label para Select2 usando stock total
        def label_inst(obj):
            stock_total = stock_por_maestro.get(obj.id, 0)
            return f"{obj.nombre_producto} - ${obj.precio_venta:,.0f} (Stock total: {stock_total})"

        self.fields['producto'].label_from_instance = label_inst

    def clean(self):
        from django.core.exceptions import ValidationError
        cleaned_data = super().clean()
        producto = cleaned_data.get('producto')  # maestro
        cantidad = cleaned_data.get('cantidad')

        if producto and cantidad:
            stock_total = self._stock_por_maestro.get(producto.id, 0)
            if cantidad > stock_total:
                raise ValidationError(
                    f'Stock insuficiente. Disponible: {stock_total} unidades'
                )

        return cleaned_data


class LoginForm(forms.Form):
    correo = forms.EmailField(
        label='Correo Electrónico',
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ingrese su correo',
            'required': 'required'
        })
    )
    password = forms.CharField(
        label='Contraseña',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ingrese su contraseña',
            'required': 'required'
        })
    )

    def clean(self):
        cleaned_data = super().clean()
        correo = cleaned_data.get('correo')
        password = cleaned_data.get('password')

        if correo and password:
            try:
                usuario = Usuarios.objects.get(correo=correo, activo=1)
                if not check_password(password, usuario.clave):
                    raise forms.ValidationError('Correo o contraseña incorrectos')
            except Usuarios.DoesNotExist:
                raise forms.ValidationError('Correo o contraseña incorrectos')

        return cleaned_data


class LoginForm(forms.Form):
    correo = forms.EmailField(
        label='Correo Electrónico',
        widget=forms.EmailInput(attrs={
            'placeholder': 'Ingrese su correo',
            'required': 'required'
        })
    )
    password = forms.CharField(
        label='Contraseña',
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Ingrese su contraseña',
            'required': 'required'
        })
    )
    
    def clean(self):
        cleaned_data = super().clean()
        correo = cleaned_data.get('correo')
        password = cleaned_data.get('password')
        
        if correo and password:
            try:
                usuario = Usuarios.objects.get(correo=correo, activo=1)
                if not check_password(password, usuario.clave):
                    raise forms.ValidationError('Correo o contraseña incorrectos')
            except Usuarios.DoesNotExist:
                raise forms.ValidationError('Correo o contraseña incorrectos')
        
        return cleaned_data

class UsuarioForm(forms.ModelForm):
    # Validador para teléfono (solo 10 dígitos)
    telefono_validator = RegexValidator(
        regex=r'^\d{10}$',
        message='El teléfono debe tener exactamente 10 dígitos'
    )
    
    # Validador para número de identificación (máximo 11 dígitos)
    identificacion_validator = RegexValidator(
        regex=r'^\d{1,11}$',
        message='El número de identificación debe tener máximo 11 dígitos'
    )
    
    num_identificacion = forms.CharField(
        max_length=11,
        validators=[identificacion_validator],
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ej: 12345678901',
            'maxlength': '11',
            'pattern': '[0-9]*',
            'inputmode': 'numeric'
        })
    )
    
    tipo_usu = forms.ChoiceField(
        choices=[
            ('administrador', 'Administrador'),
            ('operario', 'Operario')
        ],
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    p_nombre = forms.CharField(
        max_length=50,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Primer nombre'
        })
    )
    
    s_nombre = forms.CharField(
        max_length=50,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Segundo nombre (opcional)'
        })
    )
    
    p_apellido = forms.CharField(
        max_length=50,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Primer apellido'
        })
    )
    
    s_apellido = forms.CharField(
        max_length=50,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Segundo apellido (opcional)'
        })
    )
    
    correo = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'correo@ejemplo.com'
        })
    )
    
    telefono = forms.CharField(
        max_length=10,
        validators=[telefono_validator],
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '3001234567',
            'maxlength': '10',
            'pattern': '[0-9]*',
            'inputmode': 'numeric'
        })
    )
    
    direccion = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Dirección completa'
        })
    )
    
    salario = forms.DecimalField(
        max_digits=10,
        decimal_places=2,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': '1500000',
            'step': '0.01'
        })
    )
    
    fecha_nacimiento = forms.DateField(
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date',
            'id': 'fecha_nacimiento'
        })
    )
    
    activo = forms.ChoiceField(
        choices=[(1, 'Activo'), (0, 'Inactivo')],
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Contraseña',
            'id': 'password_input'
        }),
        help_text='Debe contener al menos 1 mayúscula y 3 números'
    )
    
    password_confirm = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Confirmar contraseña',
            'id': 'password_confirm_input'
        }),
        label='Confirmar Contraseña'
    )
    
    class Meta:
        model = Usuarios
        fields = [
            'num_identificacion', 'tipo_usu', 'p_nombre', 's_nombre',
            'p_apellido', 's_apellido', 'correo', 'telefono',
            'direccion', 'salario', 'fecha_nacimiento', 'activo'
        ]
    
    def clean_num_identificacion(self):
        """Valida que el número de identificación sea único y válido"""
        num_id = self.cleaned_data.get('num_identificacion')
        
        if not num_id.isdigit():
            raise ValidationError('El número de identificación solo puede contener dígitos')
        
        if len(num_id) > 11:
            raise ValidationError('El número de identificación no puede tener más de 11 dígitos')
        
        # Verificar si ya existe (excepto en edición)
        if self.instance.pk:
            if Usuarios.objects.exclude(pk=self.instance.pk).filter(num_identificacion=num_id).exists():
                raise ValidationError('Este número de identificación ya está registrado')
        else:
            if Usuarios.objects.filter(num_identificacion=num_id).exists():
                raise ValidationError('Este número de identificación ya está registrado')
        
        return num_id
    
    def clean_telefono(self):
        """Valida que el teléfono tenga exactamente 10 dígitos"""
        telefono = self.cleaned_data.get('telefono')
        
        if not telefono.isdigit():
            raise ValidationError('El teléfono solo puede contener números')
        
        if len(telefono) != 10:
            raise ValidationError('El teléfono debe tener exactamente 10 dígitos')
        
        return telefono
    
    def clean_fecha_nacimiento(self):
        """Valida que el usuario sea mayor de 18 años"""
        fecha_nac = self.cleaned_data.get('fecha_nacimiento')
        
        if fecha_nac:
            hoy = date.today()
            edad = relativedelta(hoy, fecha_nac).years
            
            if edad < 18:
                raise ValidationError(
                    f'El usuario debe ser mayor de edad. Edad actual: {edad} años'
                )
            
            if edad > 100:
                raise ValidationError('La fecha de nacimiento no es válida')
        
        return fecha_nac
    
    def clean_password(self):
        """Valida que la contraseña tenga al menos 1 mayúscula y 3 números"""
        password = self.cleaned_data.get('password')
        
        if not password:
            raise ValidationError('La contraseña es obligatoria')
        
        # Verificar longitud mínima
        if len(password) < 8:
            raise ValidationError('La contraseña debe tener al menos 8 caracteres')
        
        # Contar mayúsculas
        mayusculas = sum(1 for c in password if c.isupper())
        if mayusculas < 1:
            raise ValidationError('La contraseña debe contener al menos 1 letra mayúscula')
        
        # Contar números
        numeros = sum(1 for c in password if c.isdigit())
        if numeros < 3:
            raise ValidationError('La contraseña debe contener al menos 3 números')
        
        return password
    
    def clean(self):
        """Validación general del formulario"""
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password_confirm = cleaned_data.get('password_confirm')
        
        if password and password_confirm:
            if password != password_confirm:
                raise ValidationError('Las contraseñas no coinciden')
        
        return cleaned_data