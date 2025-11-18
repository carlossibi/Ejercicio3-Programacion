import threading
import time
import datetime

# Simulación de fichero grande
file_name = 'fichero_grande.txt'
num_lines = 50000
keyword = 'ERROR'

with open(file_name, 'w') as f:
    for i in range(num_lines):
        if i % 100 == 0:  # Cada 100 líneas incluimos "ERROR"
            f.write(f'Esta linea contiene un {keyword}\n')
        else:
            f.write(f'Esta linea no contiene la palabra clave {i}\n')

contador = 0 #Contador de las líneas de error 
semaforo = threading.Semaphore() #No permite que dos hilos accedan a la misma variable  

def hilo_secundario(): #Abre el archivo y lee cada línea
    global contador
    with open(file_name, 'r') as f:
        for linea in f:
            time.sleep(0.001)  # Simular procesamiento lento
            if keyword in linea:
                semaforo.acquire()
                contador += 1
                semaforo.release() #Utiliza un semaforo para modificar el contador

def menu(): #Menú principal
    print("\nMenú:")
    print("1. Mostrar la hora actual")
    print("2. Mostrar mensaje")
    print("3. Salir")

thread = threading.Thread(target=hilo_secundario) #Crea el hilo para cuente "Error"
thread.start() #Arranca el hilo secundario

while thread.is_alive():
    menu()
    opcion = input("Seleccione una opción: ")
    if opcion == '1':
        print("Hora actual: ", datetime.datetime.now().strftime('%H:%M:%S'))
    elif opcion == '2':
        print("Este es un mensaje de prueba.")
    elif opcion == '3':
        print("Saliendo...")
        break
    else:
        print("Opción no válida. Intente de nuevo.")

thread.join() #Espera al hilo antes de mostrar el resultado
print(f'Número total de líneas con la palabra "{keyword}": {contador}') #Muestra líneas con error