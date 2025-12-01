import os
import django
import pandas as pd

# Inicializar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ufc_app.settings')
django.setup()

# Importar el modelo
from peleadores.models import Peleador

# Ruta al CSV
csv_path = r"C:\Users\kddhd\Downloads\ufc_peleadores.csv"  # Nota la r delante de la ruta para evitar problemas con '\'

# Leer el CSV
df = pd.read_csv(csv_path)

# Iterar y crear/actualizar peleadores
for _, row in df.iterrows():
    # Ignorar filas sin nombre
    if pd.isna(row['name']):
        continue

    peleador, created = Peleador.objects.update_or_create(
        nombre=row['name'],
        defaults={
            'victorias': row['wins'] if not pd.isna(row['wins']) else 0,
            'derrotas': row['losses'] if not pd.isna(row['losses']) else 0,
            'altura': row['height'] if not pd.isna(row['height']) else None,
            'peso': row['weight'] if not pd.isna(row['weight']) else None,
            'alcance': row['reach'] if not pd.isna(row['reach']) else None,
            'guardia': row['stance'] if not pd.isna(row['stance']) else None,
            'edad': row['age'] if not pd.isna(row['age']) else None,
            'golpes_por_minuto': row['SLpM'] if not pd.isna(row['SLpM']) else None,
            'precision_golpes': row['sig_str_acc'] if not pd.isna(row['sig_str_acc']) else None,
            'golpes_recibidos': row['SApM'] if not pd.isna(row['SApM']) else None,
            'defensa_golpes': row['str_def'] if not pd.isna(row['str_def']) else None,
            'derribos_promedio': row['td_avg'] if not pd.isna(row['td_avg']) else None,
            'precision_derribos': row['td_acc'] if not pd.isna(row['td_acc']) else None,
            'defensa_derribos': row['td_def'] if not pd.isna(row['td_def']) else None,
            'sumisiones_promedio': row['sub_avg'] if not pd.isna(row['sub_avg']) else None
        }
    )
    if created:
        print(f'{peleador.nombre} creado')
    else:
        print(f'{peleador.nombre} actualizado')

print("✅ Importación completada correctamente.")
