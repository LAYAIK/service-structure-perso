from django.db import models
import uuid

class Structure(models.Model):
    id_structure = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nom = models.CharField(max_length=100)
    definition = models.CharField(blank=True, null=True, max_length=255)
    description = models.CharField(blank=True, null=True, max_length=255)
    date_creation = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return str(self.id_structure)
    
    
class HistoriqueStructure(models.Model):
    id_historique = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    id_structure = models.UUIDField(null=True)
    action = models.CharField(max_length=200, null=False)
    date_action = models.DateTimeField(auto_now_add=True)
    id_utilisateur = models.UUIDField(null=False)
    note = models.CharField(max_length=255, null=True)
    nom = models.CharField(max_length=100)
    definition = models.CharField(blank=True, null=True, max_length=255)
    
    def __str__(self):
        return str(self.id_historique)
