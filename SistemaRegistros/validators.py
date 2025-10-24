"""
Validadores personalizados para el sistema de registro de visitas
"""

from django.core.exceptions import ValidationError
import re


def validar_rut_chileno(rut):
    """
    Valida el formato y dígito verificador de un RUT chileno.
    
    Formatos aceptados:
    - 12345678-9
    - 12.345.678-9
    - 12345678-K
    
    Args:
        rut (str): RUT a validar
        
    Raises:
        ValidationError: Si el RUT no es válido
    """
    
    if not rut:
        raise ValidationError('El RUT es obligatorio.')
    
    # Limpiar el RUT (eliminar puntos y convertir a mayúsculas)
    rut_limpio = rut.replace('.', '').replace('-', '').upper().strip()
    
    # Validar formato básico (debe tener entre 8 y 9 caracteres)
    if len(rut_limpio) < 8 or len(rut_limpio) > 9:
        raise ValidationError('El RUT debe tener el formato correcto (ej: 12345678-9)')
    
    # Separar número y dígito verificador
    numero = rut_limpio[:-1]
    dv_ingresado = rut_limpio[-1]
    
    # Validar que el número sea numérico
    if not numero.isdigit():
        raise ValidationError('El RUT debe contener solo números antes del guión.')
    
    # Validar que el dígito verificador sea válido (0-9 o K)
    if dv_ingresado not in '0123456789K':
        raise ValidationError('El dígito verificador debe ser un número entre 0-9 o K.')
    
    # Calcular el dígito verificador esperado
    dv_calculado = calcular_digito_verificador(numero)
    
    # Comparar el dígito verificador ingresado con el calculado
    if dv_ingresado != dv_calculado:
        raise ValidationError(
            f'El RUT {rut} no es válido. Dígito verificador incorrecto.'
        )
    
    return True


def calcular_digito_verificador(rut_sin_dv):
    """
    Calcula el dígito verificador de un RUT chileno.
    
    Args:
        rut_sin_dv (str): RUT sin dígito verificador (solo números)
        
    Returns:
        str: Dígito verificador calculado ('0'-'9' o 'K')
    """
    
    # Convertir a entero
    rut_numero = int(rut_sin_dv)
    
    # Algoritmo de cálculo del módulo 11
    suma = 0
    multiplicador = 2
    
    # Recorrer el RUT de derecha a izquierda
    while rut_numero > 0:
        suma += (rut_numero % 10) * multiplicador
        rut_numero //= 10
        multiplicador += 1
        if multiplicador > 7:
            multiplicador = 2
    
    # Calcular el dígito verificador
    resto = suma % 11
    dv = 11 - resto
    
    # Casos especiales
    if dv == 11:
        return '0'
    elif dv == 10:
        return 'K'
    else:
        return str(dv)


def formatear_rut(rut):
    """
    Formatea un RUT chileno al formato estándar 12.345.678-9
    
    Args:
        rut (str): RUT sin formato
        
    Returns:
        str: RUT formateado
    """
    
    # Limpiar el RUT
    rut_limpio = rut.replace('.', '').replace('-', '').upper().strip()
    
    if len(rut_limpio) < 8:
        return rut
    
    # Separar número y dígito verificador
    numero = rut_limpio[:-1]
    dv = rut_limpio[-1]
    
    # Formatear con puntos
    numero_formateado = ''
    for i, digito in enumerate(reversed(numero)):
        if i > 0 and i % 3 == 0:
            numero_formateado = '.' + numero_formateado
        numero_formateado = digito + numero_formateado
    
    return f"{numero_formateado}-{dv}"


def validar_formato_rut(rut):
    """
    Valida que el RUT tenga un formato válido con regex.
    
    Args:
        rut (str): RUT a validar
        
    Returns:
        bool: True si el formato es válido
        
    Raises:
        ValidationError: Si el formato no es válido
    """
    
    # Patrones válidos:
    # - 12345678-9
    # - 12.345.678-9
    patron = r'^\d{1,2}\.?\d{3}\.?\d{3}-[\dKk]$'
    
    if not re.match(patron, rut):
        raise ValidationError(
            'El RUT debe tener el formato: 12345678-9 o 12.345.678-9'
        )
    
    return True


# Ejemplos de uso:
if __name__ == '__main__':
    # Casos de prueba
    ruts_validos = [
        '18.765.432-1',
        '12345678-5',
        '7654321-K',
    ]
    
    ruts_invalidos = [
        '18.765.432-2',  # DV incorrecto
        '12345678-K',    # DV incorrecto
        'abcdefgh-9',    # Formato inválido
    ]
    
    print("=== RUTs Válidos ===")
    for rut in ruts_validos:
        try:
            validar_rut_chileno(rut)
            print(f"✓ {rut} es válido → Formateado: {formatear_rut(rut)}")
        except ValidationError as e:
            print(f"✗ {rut}: {e}")
    
    print("\n=== RUTs Inválidos ===")
    for rut in ruts_invalidos:
        try:
            validar_rut_chileno(rut)
            print(f"✓ {rut} es válido")
        except ValidationError as e:
            print(f"✗ {rut}: {e}")
