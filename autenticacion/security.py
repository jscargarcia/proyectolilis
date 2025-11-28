"""
Utilidades para sanitización y validación de seguridad
Cumple con casos S-VAL-01 y S-VAL-02
"""

import re
import html
from django.utils.html import strip_tags
from django.core.exceptions import ValidationError


class SanitizadorInput:
    """
    Clase para sanitizar inputs y prevenir ataques XSS y SQL Injection
    """
    
    # Patrones peligrosos comunes en ataques
    PATRONES_SQL_INJECTION = [
        r"(\b(SELECT|INSERT|UPDATE|DELETE|DROP|CREATE|ALTER|EXEC|EXECUTE)\b)",
        r"(--|\#|\/\*|\*\/)",
        r"(\b(OR|AND)\b\s*\d+\s*=\s*\d+)",
        r"(\b(UNION|JOIN)\b)",
        r"(;\s*(DROP|DELETE|TRUNCATE))",
    ]
    
    PATRONES_XSS = [
        r"<script[^>]*>.*?</script>",
        r"javascript:",
        r"on\w+\s*=",  # onclick, onload, etc.
        r"<iframe[^>]*>",
        r"<object[^>]*>",
        r"<embed[^>]*>",
    ]
    
    @classmethod
    def detectar_sql_injection(cls, texto):
        """
        Detecta posibles intentos de SQL Injection
        Caso S-VAL-01
        
        Args:
            texto: String a validar
            
        Returns:
            tuple: (es_sospechoso: bool, patron_detectado: str)
        """
        if not texto or not isinstance(texto, str):
            return False, None
        
        texto_upper = texto.upper()
        
        for patron in cls.PATRONES_SQL_INJECTION:
            if re.search(patron, texto_upper, re.IGNORECASE):
                return True, patron
        
        return False, None
    
    @classmethod
    def detectar_xss(cls, texto):
        """
        Detecta posibles intentos de XSS
        Caso S-VAL-02
        
        Args:
            texto: String a validar
            
        Returns:
            tuple: (es_sospechoso: bool, patron_detectado: str)
        """
        if not texto or not isinstance(texto, str):
            return False, None
        
        for patron in cls.PATRONES_XSS:
            if re.search(patron, texto, re.IGNORECASE):
                return True, patron
        
        return False, None
    
    @classmethod
    def sanitizar_texto(cls, texto, permitir_html=False):
        """
        Sanitiza un texto removiendo contenido peligroso
        
        Args:
            texto: String a sanitizar
            permitir_html: Si se permite HTML seguro (solo tags básicos)
            
        Returns:
            str: Texto sanitizado
        """
        if not texto or not isinstance(texto, str):
            return texto
        
        # Verificar SQL Injection
        es_sql_injection, _ = cls.detectar_sql_injection(texto)
        if es_sql_injection:
            raise ValidationError(
                'El texto contiene caracteres no permitidos. '
                'Por favor revisa tu entrada.'
            )
        
        # Verificar XSS
        es_xss, _ = cls.detectar_xss(texto)
        if es_xss:
            # Remover scripts y código peligroso
            texto = re.sub(r'<script[^>]*>.*?</script>', '', texto, flags=re.IGNORECASE | re.DOTALL)
            texto = re.sub(r'javascript:', '', texto, flags=re.IGNORECASE)
            texto = re.sub(r'on\w+\s*=\s*["\'][^"\']*["\']', '', texto, flags=re.IGNORECASE)
        
        if not permitir_html:
            # Remover todas las etiquetas HTML
            texto = strip_tags(texto)
            # Escapar caracteres especiales HTML
            texto = html.escape(texto)
        else:
            # Solo permitir tags seguros
            tags_permitidos = ['b', 'i', 'u', 'strong', 'em', 'p', 'br']
            # Implementar whitelist de tags (simplificado)
            texto = strip_tags(texto)  # Por seguridad, remover todo
        
        return texto.strip()
    
    @classmethod
    def validar_input_seguro(cls, texto, campo_nombre='campo'):
        """
        Valida que un input sea seguro, lanzando excepción si no lo es
        
        Args:
            texto: String a validar
            campo_nombre: Nombre del campo para mensajes de error
            
        Raises:
            ValidationError: Si el input es peligroso
        """
        if not texto:
            return
        
        # Detectar SQL Injection
        es_sql_injection, patron = cls.detectar_sql_injection(texto)
        if es_sql_injection:
            raise ValidationError(
                f'El {campo_nombre} contiene patrones no permitidos. '
                f'Por favor evita usar caracteres especiales de SQL.'
            )
        
        # Detectar XSS
        es_xss, patron = cls.detectar_xss(texto)
        if es_xss:
            raise ValidationError(
                f'El {campo_nombre} contiene código HTML o JavaScript no permitido. '
                f'Por favor ingresa solo texto plano.'
            )
    
    @classmethod
    def sanitizar_diccionario(cls, datos, campos_permitir_html=None):
        """
        Sanitiza todos los valores string de un diccionario
        
        Args:
            datos: Diccionario con datos a sanitizar
            campos_permitir_html: Lista de campos que permiten HTML
            
        Returns:
            dict: Diccionario sanitizado
        """
        if campos_permitir_html is None:
            campos_permitir_html = []
        
        datos_limpios = {}
        for key, value in datos.items():
            if isinstance(value, str):
                permitir_html = key in campos_permitir_html
                datos_limpios[key] = cls.sanitizar_texto(value, permitir_html)
            elif isinstance(value, dict):
                datos_limpios[key] = cls.sanitizar_diccionario(value, campos_permitir_html)
            elif isinstance(value, list):
                datos_limpios[key] = [
                    cls.sanitizar_texto(item, False) if isinstance(item, str) else item
                    for item in value
                ]
            else:
                datos_limpios[key] = value
        
        return datos_limpios


def validar_sin_sql_injection(value):
    """
    Validador Django para campos de formulario
    Uso: validators=[validar_sin_sql_injection]
    """
    SanitizadorInput.validar_input_seguro(value, 'campo')


def validar_sin_xss(value):
    """
    Validador Django para campos de formulario que no permiten HTML
    Uso: validators=[validar_sin_xss]
    """
    es_xss, _ = SanitizadorInput.detectar_xss(value)
    if es_xss:
        raise ValidationError(
            'Este campo no permite código HTML o JavaScript.'
        )


# Decorador para views
def sanitizar_request_data(view_func):
    """
    Decorador para sanitizar automáticamente los datos del request
    
    Uso:
        @sanitizar_request_data
        def mi_vista(request):
            # request.POST y request.GET estarán sanitizados
            ...
    """
    from functools import wraps
    from django.http import QueryDict
    
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        # Sanitizar GET
        if request.GET:
            get_data = dict(request.GET)
            get_limpio = SanitizadorInput.sanitizar_diccionario(get_data)
            request.GET = QueryDict(mutable=True)
            for key, value in get_limpio.items():
                request.GET[key] = value
            request.GET._mutable = False
        
        # Sanitizar POST
        if request.POST:
            post_data = dict(request.POST)
            # Permitir HTML en campos de descripción/observaciones
            campos_html = ['descripcion', 'observaciones', 'notas', 'comentarios']
            post_limpio = SanitizadorInput.sanitizar_diccionario(post_data, campos_html)
            request.POST = QueryDict(mutable=True)
            for key, value in post_limpio.items():
                request.POST[key] = value
            request.POST._mutable = False
        
        return view_func(request, *args, **kwargs)
    
    return wrapper
