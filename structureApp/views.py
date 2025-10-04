from rest_framework import viewsets
from .models import Structure, HistoriqueStructure
from .serializers import StructureSerializer, HistoriqueStructureSerializer
from django.utils import timezone
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework.response import Response
from rest_framework import status
from django.db import transaction


class StructureViewSet(viewsets.ModelViewSet):
    queryset = Structure.objects.all()
    serializer_class = StructureSerializer
    
    @extend_schema(
        summary="Liste des structures",
        description="Récupère la liste de toutes les structures.",
        parameters=[
            OpenApiParameter(name='search', description='Recherche par nom de structure', required=False, type=str),
        ],
        responses={200: StructureSerializer(many=True)},
    )
    def list(self, request, *args, **kwargs):
        search = request.GET.get('search')
        if search:
            self.queryset = self.queryset.filter(name__icontains=search)
        return super().list(request, *args, **kwargs)
    
    @extend_schema(
        summary= "créer une structure",
        description="Crée une nouvelle structure.",
        request=StructureSerializer,
        responses={201: StructureSerializer},
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
    
    @extend_schema(
        summary="Modifier une structure",
        description="Modifie une structure existante.",
        request=StructureSerializer,
        responses={200: StructureSerializer},
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)
    
    @extend_schema(
        summary="Détails d'une structure",
        description="Récupère les détails d'une structure.",
        responses={200: StructureSerializer},
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
    
    
    @extend_schema(
    summary="Supprimer une structure",
    description="Supprime une structure.",
    responses={204: None},
    )
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()  # Récupère la structure à supprimer

        try:

            # --- Extraction sûre du payload ---
            note = "Structure supprimée"

            if isinstance(request.data, dict):
                id_utilisateur = request.data.get("id_utilisateur")
                note = request.data.get("note", note)

            # fallback si utilisateur authentifié
            if not id_utilisateur and request.user.is_authenticated:
                id_utilisateur = request.user.id

            with transaction.atomic():
                # 1. Sauvegarder dans l'historique
                HistoriqueStructure.objects.create(
                    nom=instance.nom,
                    definition=instance.definition,
                    date_action=timezone.now(),
                    action="Suppression",
                    id_utilisateur=id_utilisateur,
                    id_structure=instance.id_structure,
                    note=note,
                )

                # 2. Supprimer la structure
                self.perform_destroy(instance)

            return Response(status=status.HTTP_204_NO_CONTENT, data={"message": "Structure supprimée avec succès."})

        except Exception as e:
            import traceback
            print("ERREUR destroy:", traceback.format_exc())  # Debug console
            return Response(
                {"error": f"Suppression annulée : {str(e)}"},
                status=status.HTTP_400_BAD_REQUEST,
            )

    
    @extend_schema(
        summary="Recupere une structure",
        description="Récupère une structure.",
        responses={200: StructureSerializer},
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
    
