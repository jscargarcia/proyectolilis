"""
Utilidades para validación de RUT chileno
"""

def validar_rut(rut):
    """
    Valida un RUT chileno
    Args:
        rut (str): RUT con o sin puntos y guión
    Returns:
        tuple: (es_valido, rut_formateado, mensaje_error)
    """
    if not rut:
        return False, "", "RUT es obligatorio"
    
    # Limpiar el RUT
    rut_limpio = rut.replace(".", "").replace("-", "").replace(" ", "").upper()
    
    # Verificar largo mínimo
    if len(rut_limpio) < 8:
        return False, rut, "RUT debe tener al menos 8 dígitos"
    
    if len(rut_limpio) > 9:
        return False, rut, "RUT no puede tener más de 9 dígitos"
    
    # Separar cuerpo y dígito verificador
    try:
        cuerpo = rut_limpio[:-1]
        dv = rut_limpio[-1]
        
        # Verificar que el cuerpo sean solo números
        if not cuerpo.isdigit():
            return False, rut, "El cuerpo del RUT debe contener solo números"
        
        # Calcular dígito verificador
        suma = 0
        multiplicador = 2
        
        for i in range(len(cuerpo) - 1, -1, -1):
            suma += int(cuerpo[i]) * multiplicador
            multiplicador += 1
            if multiplicador > 7:
                multiplicador = 2
        
        resto = suma % 11
        dv_calculado = 11 - resto
        
        if dv_calculado == 11:
            dv_esperado = "0"
        elif dv_calculado == 10:
            dv_esperado = "K"
        else:
            dv_esperado = str(dv_calculado)
        
        # Verificar dígito verificador
        if dv != dv_esperado:
            return False, rut, f"Dígito verificador incorrecto. Debería ser {dv_esperado}"
        
        # Formatear RUT
        rut_formateado = formatear_rut(cuerpo + dv)
        
        return True, rut_formateado, ""
        
    except (ValueError, IndexError) as e:
        return False, rut, "Formato de RUT inválido"


def formatear_rut(rut):
    """
    Formatea un RUT agregando puntos y guión
    Args:
        rut (str): RUT sin formato
    Returns:
        str: RUT formateado (ej: 12.345.678-9)
    """
    if not rut:
        return rut
    
    rut_limpio = rut.replace(".", "").replace("-", "").replace(" ", "").upper()
    
    if len(rut_limpio) < 8:
        return rut
    
    cuerpo = rut_limpio[:-1]
    dv = rut_limpio[-1]
    
    # Agregar puntos cada 3 dígitos desde la derecha
    cuerpo_formateado = ""
    for i, digito in enumerate(reversed(cuerpo)):
        if i > 0 and i % 3 == 0:
            cuerpo_formateado = "." + cuerpo_formateado
        cuerpo_formateado = digito + cuerpo_formateado
    
    return f"{cuerpo_formateado}-{dv}"


def limpiar_rut(rut):
    """
    Limpia un RUT removiendo puntos y guión
    Args:
        rut (str): RUT con formato
    Returns:
        str: RUT sin formato
    """
    if not rut:
        return ""
    
    return rut.replace(".", "").replace("-", "").replace(" ", "").upper()


# Función para validar RUT chileno específicamente
def es_rut_chileno_valido(rut):
    """
    Verifica si un RUT corresponde al formato chileno válido
    Args:
        rut (str): RUT a validar
    Returns:
        bool: True si es un RUT chileno válido
    """
    es_valido, _, _ = validar_rut(rut)
    return es_valido