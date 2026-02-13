# Esto es un comentario, no hace nada, es para nosotros
nombre = "Lu"          # Un texto (String)
edad = 25              # Un número entero (Integer)
estudiante = True      # Un valor de verdad (Boolean)

# Para ver el resultado en pantalla usamos print()
print(f"Hola, mi nombre es {nombre} y tengo {edad} años. ❤️")

precio_original = 100
descuento = precio_original * 0.10
precio_final = precio_original - descuento

# La magia para escribir en el README.md
mensaje = f"# Resultado del Curso\n\nEl precio final calculado es: **{precio_final} euros**. ❤️"

with open("README.md", "w") as archivo:
    archivo.write(mensaje)
