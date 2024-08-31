import os
import requests
from datetime import datetime, timedelta
from PIL import Image

def download_images_and_create_gif(start_datetime, end_datetime, radar_type, interval_minutes=10):
    # Crear el nombre del directorio basado en el radar y la fecha y hora actual
    timestamp_str = datetime.now().strftime('%Y%m%d%H%M%S')
    output_dir = f"{radar_type}_{timestamp_str}"
    
    # Crear el directorio para guardar las imágenes
    os.makedirs(output_dir, exist_ok=True)

    # Base URL template
    url_template = f"https://www.aemet.es/imagenes_d/eltiempo/observacion/radar/{{date}}{{hour:02d}}{{minute:02d}}_r8{radar_type}.gif"

    # Descargar imágenes
    image_paths = []
    current_time = start_datetime
    while current_time <= end_datetime:
        date_str = current_time.strftime('%Y%m%d')
        image_url = url_template.format(date=date_str, hour=current_time.hour, minute=current_time.minute)
        image_name = f"{current_time.strftime('%Y%m%d_%H%M')}_r8{radar_type}.gif"
        save_path = os.path.join(output_dir, image_name)
        
        response = requests.get(image_url)
        if response.status_code == 200:
            with open(save_path, 'wb') as file:
                file.write(response.content)
            image_paths.append(save_path)
            print(f"Descargada: {image_name}")
        else:
            print(f"Fallo al descargar: {image_name}")
        
        current_time += timedelta(minutes=interval_minutes)

    # Crear un GIF animado
    if image_paths:
        images = [Image.open(img_path) for img_path in image_paths]
        gif_filename = "radar_animation.gif"
        gif_path = os.path.join(output_dir, gif_filename)
        images[0].save(
            gif_path, save_all=True, append_images=images[1:], duration=500, loop=0
        )
        print(f"GIF creado: {gif_path}")
    else:
        print("No se descargaron imágenes, no se creó el GIF.")

# Pedir al usuario las fechas y horas de inicio y fin
print("Introduce las fechas y horas en formato UTC (Coordinated Universal Time).")
print("Por ejemplo, si estás en España, la hora local es UTC+2 en verano y UTC+1 en invierno.")
print("El dia debe ser el mismo en ambas fechas.")
print("Si quieres otra fecha deberas crear 2 gif separados y luego unirlos con un editor de video.")
start_date = input("Introduce la fecha de inicio (UTC) (YYYY-MM-DD): ")
start_time = input("Introduce la hora de inicio (UTC) (HH:MM): ")
end_date = input("Introduce la fecha de fin (UTC) (YYYY-MM-DD): ")
end_time = input("Introduce la hora de fin (UTC) (HH:MM): ")

# Pedir al usuario el tipo de radar
radar_type = input("Introduce el tipo de radar (mu, za, va, etc.): ")

# Convertir las entradas en objetos datetime
start_datetime = datetime.strptime(f"{start_date} {start_time}", '%Y-%m-%d %H:%M')
end_datetime = datetime.strptime(f"{end_date} {end_time}", '%Y-%m-%d %H:%M')

# Llamar a la función principal
download_images_and_create_gif(start_datetime, end_datetime, radar_type)