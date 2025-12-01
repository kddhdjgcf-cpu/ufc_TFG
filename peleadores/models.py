from django.db import models

class Peleador(models.Model):
    foto = models.ImageField(upload_to='peleadores/', blank=True, null=True)
    nombre = models.CharField(max_length=100)
    victorias = models.IntegerField(default=0)
    derrotas = models.IntegerField(default=0)
    altura = models.FloatField(null=True, blank=True)  # en cm
    peso = models.FloatField(null=True, blank=True)    # en kg
    alcance = models.FloatField(null=True, blank=True) # en cm
    guardia = models.CharField(max_length=50, null=True, blank=True)  # Orthodox / Southpaw
    edad = models.IntegerField(null=True, blank=True)

    golpes_por_minuto = models.FloatField(null=True, blank=True)       # SLpM - Golpes significativos por minuto
    precision_golpes = models.FloatField(null=True, blank=True)        # sig_str_acc - Precisión de golpeo
    golpes_recibidos = models.FloatField(null=True, blank=True)        # SApM - Golpes recibidos por minuto
    defensa_golpes = models.FloatField(null=True, blank=True)          # str_def - % de defensa de golpes
    derribos_promedio = models.FloatField(null=True, blank=True)       # td_avg - Derribos promedio por 15 min
    precision_derribos = models.FloatField(null=True, blank=True)      # td_acc - Precisión de derribos
    defensa_derribos = models.FloatField(null=True, blank=True)        # td_def - % de defensa de derribos
    sumisiones_promedio = models.FloatField(null=True, blank=True)     # sub_avg - Sumisiones promedio por 15 min

    def __str__(self):
        return self.nombre