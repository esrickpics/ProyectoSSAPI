from django.db import models
from django.core.exceptions import ValidationError
from activos.models import Activo


class Mantenimiento(models.Model):
    """Registro de mantenimientos de activos"""
    
    class EstadoMantenimiento(models.TextChoices):
        EN_PROCESO = 'EP', 'En proceso'
        FINALIZADO = 'FI', 'Finalizado'
    
    activo = models.ForeignKey(
        Activo,
        on_delete=models.CASCADE,
        related_name='mantenimientos',
        verbose_name='Activo'
    )
    tecnico = models.CharField(max_length=150, verbose_name='Técnico')
    telefono = models.CharField(max_length=20, verbose_name='Teléfono')
    descripcion = models.TextField(verbose_name='Descripción del Mantenimiento')
    costo = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='Costo'
    )
    fecha = models.DateField(auto_now_add=True, verbose_name='Fecha de Registro')
    estado = models.CharField(
        max_length=2,
        choices=EstadoMantenimiento.choices,
        default=EstadoMantenimiento.EN_PROCESO,
        verbose_name='Estado'
    )
    
    # Campos de auditoría
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Mantenimiento"
        verbose_name_plural = "Mantenimientos"
        ordering = ['-fecha']
        indexes = [
            models.Index(fields=['activo', '-fecha']),
            models.Index(fields=['estado']),
        ]
    
    def __str__(self):
        return f"{self.activo.codigo_inventario} - {self.tecnico} - {self.fecha.strftime('%d/%m/%Y')}"
    
    def save(self, *args, **kwargs):
        """
        Sobrescribimos save() para actualizar automáticamente el estado del activo
        """
        # Guardar el mantenimiento primero
        super().save(*args, **kwargs)
        
        # Actualizar el estado del activo según el estado del mantenimiento
        if self.estado == self.EstadoMantenimiento.EN_PROCESO:
            # Si el mantenimiento está en proceso, el activo pasa a "En Mantenimiento"
            if self.activo.estado != Activo.EstadoActivo.EN_MANTENIMIENTO:
                self.activo.estado = Activo.EstadoActivo.EN_MANTENIMIENTO
                self.activo.save(update_fields=['estado', 'fecha_actualizacion'])
        
        elif self.estado == self.EstadoMantenimiento.FINALIZADO:
            # Si el mantenimiento finalizó, verificar si hay otros mantenimientos en proceso
            mantenimientos_en_proceso = Mantenimiento.objects.filter(
                activo=self.activo,
                estado=self.EstadoMantenimiento.EN_PROCESO
            ).exclude(pk=self.pk).exists()
            
            # Solo volver a "Activo" si no hay otros mantenimientos en proceso
            if not mantenimientos_en_proceso:
                if self.activo.estado == Activo.EstadoActivo.EN_MANTENIMIENTO:
                    self.activo.estado = Activo.EstadoActivo.ACTIVO
                    self.activo.save(update_fields=['estado', 'fecha_actualizacion'])
    
    def clean(self):
        """Validaciones personalizadas"""
        super().clean()
        
        # Validar que el costo sea positivo
        if self.costo is not None and self.costo < 0:
            raise ValidationError({'costo': 'El costo no puede ser negativo.'})