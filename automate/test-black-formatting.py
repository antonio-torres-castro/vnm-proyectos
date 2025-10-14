#!/usr/bin/env python3
"""
Script de prueba para verificar que Black está formateando correctamente.
Este archivo tiene líneas largas que deben ser formateadas automáticamente por Black al guardar.
"""

# Esta línea es muy larga y debería ser formateada automáticamente cuando guardes el archivo - exceeds 79 characters limit significantly
def funcion_con_parametros_muy_largos(parametro_uno, parametro_dos, parametro_tres, parametro_cuatro, parametro_cinco):
    """Función con parámetros largos para probar el formateo."""
    resultado = f"Parámetros: {parametro_uno}, {parametro_dos}, {parametro_tres}, {parametro_cuatro}, {parametro_cinco}"
    return resultado

# Esta es otra línea muy larga que debe ser formateada - lista con muchos elementos que excede 79 caracteres
lista_muy_larga = ["elemento_uno", "elemento_dos", "elemento_tres", "elemento_cuatro", "elemento_cinco", "elemento_seis", "elemento_siete"]

# Diccionario con línea larga
diccionario_largo = {"clave_muy_larga_uno": "valor_muy_largo_uno", "clave_muy_larga_dos": "valor_muy_largo_dos", "clave_tres": "valor_tres"}

def main():
    """Función principal para probar el formateo."""
    print("🧪 Testing Black formatter...")
    
    # Llamada a función con línea larga
    resultado = funcion_con_parametros_muy_largos("valor1", "valor2", "valor3", "valor4", "valor5")
    print(f"Resultado de la función: {resultado}")
    
    # Imprimir lista
    print(f"Lista: {lista_muy_larga}")
    
    # Imprimir diccionario
    print(f"Diccionario: {diccionario_largo}")
    
    print("✅ Si ves este archivo formateado correctamente después de guardar, Black está funcionando!")

if __name__ == "__main__":
    main()
