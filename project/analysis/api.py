from django.contrib.auth.models import AnonymousUser
from django.db.models import Q
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, filters
from rest_framework.decorators import list_route
from rest_framework.response import Response
from rest_framework.decorators import detail_route
from rest_framework.exceptions import NotAcceptable

from utils.api import SiteMixin, OwnedButShareableMixin, NoPagination, PlainTextRenderer

from . import models, serializers


def owner_or_public(user):
    query = Q(public=True)
    if not isinstance(user, AnonymousUser):
        query = query | Q(owner=user)
    return query


class EncodeDatasetViewset(SiteMixin, viewsets.ReadOnlyModelViewSet):
    filter_backends = (filters.DjangoFilterBackend, )

    @list_route()
    def field_options(self, request):
        opts = models.EncodeDataset.get_field_options()
        return Response(opts)

    def get_serializer_class(self):
        return serializers.EncodeDatasetSerializer

    def get_filters(self, params):
        query = Q()

        genome_assembly = params.get('genome_assembly')
        if genome_assembly:
            query &= Q(genome_assembly=genome_assembly)

        data_type = params.getlist('data_type[]')
        if data_type:
            query &= Q(data_type__in=data_type)

        cell_type = params.getlist('cell_type[]')
        if cell_type:
            query &= Q(cell_type__in=cell_type)

        treatment = params.getlist('treatment[]')
        if treatment:
            query &= Q(treatment__in=treatment)

        antibody = params.getlist('antibody[]')
        if antibody:
            query &= Q(antibody__in=antibody)

        phase = params.getlist('phase[]')
        if phase:
            query &= Q(phase__in=phase)

        rna_extract = params.getlist('rna_extract[]')
        if rna_extract:
            query &= Q(rna_extract__in=rna_extract)

        return query

    def get_queryset(self):
        filters = self.get_filters(self.request.query_params)
        return models.EncodeDataset.objects.filter(filters)


class UserDatasetViewset(OwnedButShareableMixin, viewsets.ModelViewSet):
    pagination_class = NoPagination

    def get_serializer_class(self):
        return serializers.UserDatasetSerializer

    def get_queryset(self):
        query = owner_or_public(self.request.user)
        return models.UserDataset.objects.filter(query)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class FeatureListViewset(OwnedButShareableMixin, viewsets.ModelViewSet):
    pagination_class = NoPagination

    def get_serializer_class(self):
        return serializers.FeatureListSerializer

    def get_queryset(self):
        query = owner_or_public(self.request.user)
        return models.FeatureList.objects.filter(query)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class SortVectorViewset(OwnedButShareableMixin, viewsets.ModelViewSet):
    pagination_class = NoPagination

    def get_serializer_class(self):
        return serializers.SortVectorSerializer

    def get_queryset(self):
        query = owner_or_public(self.request.user)
        return models.SortVector.objects.filter(query)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class AnalysisViewset(OwnedButShareableMixin, viewsets.ModelViewSet):
    pagination_class = NoPagination

    @detail_route(methods=['get'])
    def plot(self, request, pk=None):
        an = get_object_or_404(models.Analysis, id=int(pk))
        return Response(an.get_summary_plot())

    @detail_route(methods=['get'])
    def sort_vector(self, request, pk=None):
        try:
            sort_vector_id = int(self.request.GET.get('id', -1))
        except:
            sort_vector_id = -1
        if sort_vector_id == -1:
            raise NotAcceptable("Sort vector `id` parameter required")
        an = get_object_or_404(models.Analysis, id=int(pk))
        return Response(an.get_sort_vector(sort_vector_id))

    def get_serializer_class(self):
        return serializers.AnalysisSerializer

    def get_queryset(self):
        query = owner_or_public(self.request.user)
        return models.Analysis.objects.filter(query)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class FeatureListCountMatrixViewset(SiteMixin, viewsets.ReadOnlyModelViewSet):

    @detail_route(methods=['get'], renderer_classes=(PlainTextRenderer,))
    def plot(self, request, pk=None):
        flcm = get_object_or_404(models.FeatureListCountMatrix, id=int(pk))
        return Response(flcm.get_dataset())

    def get_serializer_class(self):
        return serializers.FeatureListCountMatrixSerializer

    def get_queryset(self):
        return models.FeatureListCountMatrix.objects.all()
