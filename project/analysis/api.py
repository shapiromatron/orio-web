from django.contrib.auth.models import AnonymousUser
from django.db.models import Q
from rest_framework import viewsets, filters
from rest_framework.decorators import list_route
from rest_framework.response import Response
from rest_framework.decorators import detail_route
from rest_framework.exceptions import NotAcceptable

from utils.api import SiteMixin, AnalysisObjectMixin, NoPagination, PlainTextRenderer
from utils.base import try_int, is_none

from . import models, serializers


def owner_or_public(user):
    if user.is_staff:
        return Q()
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


class UserDatasetViewset(AnalysisObjectMixin, viewsets.ModelViewSet):
    pagination_class = NoPagination

    def get_serializer_class(self):
        return serializers.UserDatasetSerializer

    def get_queryset(self):
        return models.UserDataset.usable(self.request.user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class FeatureListViewset(AnalysisObjectMixin, viewsets.ModelViewSet):
    pagination_class = NoPagination

    def get_serializer_class(self):
        return serializers.FeatureListSerializer

    def get_queryset(self):
        query = owner_or_public(self.request.user)
        return models.FeatureList.objects.filter(query)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class SortVectorViewset(AnalysisObjectMixin, viewsets.ModelViewSet):
    pagination_class = NoPagination

    def get_serializer_class(self):
        return serializers.SortVectorSerializer

    def get_queryset(self):
        query = owner_or_public(self.request.user)
        return models.SortVector.objects.filter(query)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class AnalysisViewset(AnalysisObjectMixin, viewsets.ModelViewSet):
    pagination_class = NoPagination

    @detail_route(methods=['get'])
    def ks(self, request, pk=None):
        vector_id = try_int(self.request.GET.get('vector_id'), -1)
        matrix_id = try_int(self.request.GET.get('matrix_id'), -1)
        if vector_id == -1:
            raise NotAcceptable("Vector `id` parameter required")
        if matrix_id == -1:
            raise NotAcceptable("Matrix `id` parameter required")
        object = self.get_object()
        return Response(object.get_ks(vector_id, matrix_id))

    @detail_route(methods=['get'])
    def unsorted_ks(self, request, pk=None):
        matrix_id = try_int(self.request.GET.get('matrix_id'), -1)
        if matrix_id == -1:
            raise NotAcceptable("Matrix `id` parameter required")
        object = self.get_object()
        return Response(object.get_unsorted_ks(matrix_id))

    @detail_route(methods=['get'])
    def is_complete(self, request, pk=None):
        object = self.get_object()
        return Response({"is_complete": object.is_complete})

    @detail_route(methods=['get'])
    def clust_boxplot(self, request, pk=None):
        k = try_int(self.request.GET.get('k'), -1)
        col_index = try_int(self.request.GET.get('index'), -1)
        if k == -1:
            raise NotAcceptable("k parameter required")
        if col_index == -1:
            raise NotAcceptable("col_index parameter required")
        object = self.get_object()
        return Response(object.get_clust_boxplot_values(k, col_index))

    @detail_route(methods=['get'])
    def fc_vector_col_names(self, request, pk=None):
        object = self.get_object()
        return Response(object.get_fc_vectors_ngs_list())

    @detail_route(methods=['get'])
    def user_sort_ks(self, request, pk=None):
        matrix_id = try_int(self.request.GET.get('matrix_id'), -1)
        if matrix_id == -1:
            raise NotAcceptable("Matrix `id` parameter required")
        object = self.get_object()
        return Response(object.get_ks_by_user_vector(matrix_id))

    @detail_route(methods=['get'])
    def analysis_overview(self, request, pk=None):
        object = self.get_object()
        return Response(object.get_analysis_overview_init())

    @detail_route(methods=['get'])
    def individual_overview(self, request, pk=None):
        object = self.get_object()
        return Response(object.get_individual_overview_init())

    @detail_route(methods=['get'])
    def feature_clustering_overview(self, request, pk=None):
        object = self.get_object()
        return Response(object.get_feature_clustering_overview_init())

    @detail_route(methods=['get'])
    def dsc_full_row_value(self, request, pk=None):
        row_name = self.request.GET.get('row')
        object = self.get_object()
        return Response(object.get_dsc_full_row_value(row_name))

    @detail_route(methods=['get'])
    def k_clust_heatmap(self, request, pk=None):
        k_value = try_int(self.request.GET.get('k'), -1)
        if k_value == -1:
            raise NotAcceptable("k value `id` parameter required")
        dim_x = try_int(self.request.GET.get('dim_x'))
        dim_y = try_int(self.request.GET.get('dim_y'))
        object = self.get_object()
        return Response(object.get_k_clust_heatmap(k_value, dim_x, dim_y))

    @detail_route(methods=['get'])
    def feature_data(self, request, pk=None):
        feature_name = self.request.GET.get('feature')
        object = self.get_object()
        return Response(object.get_feature_data(feature_name))

    @detail_route(methods=['get'])
    def sort_vector(self, request, pk=None):
        sort_vector_id = try_int(self.request.GET.get('id'), -1)
        if sort_vector_id == -1:
            raise NotAcceptable("Sort vector `id` parameter required")
        object = self.get_object()
        return Response(object.get_sort_vector(sort_vector_id))

    @detail_route(methods=['get'], renderer_classes=(PlainTextRenderer,))
    def sortvectorscatterplot(self, request, pk=None):
        idy = try_int(self.request.GET.get('idy'))
        column = self.request.GET.get('column')
        if idy is None:
            raise NotAcceptable("Parameter `idy` is required; `column` is optional")  # noqa
        object = self.get_object()
        return Response(object.get_sortvector_scatterplot_data(idy, column))

    @detail_route(methods=['get'], renderer_classes=(PlainTextRenderer,))
    def scatterplot(self, request, pk=None):
        idx = try_int(self.request.GET.get('idx'))
        idy = try_int(self.request.GET.get('idy'))
        column = self.request.GET.get('column')
        if idx is None or idy is None:
            raise NotAcceptable("Parameters `idx` and `idy` are required")
        object = self.get_object()
        return Response(object.get_scatterplot_data(idx, idy, column))

    @detail_route(methods=['get'])
    def bin_names(self, request, pk=None):
        object = self.get_object()
        return Response(object.get_bin_names())

    @detail_route(methods=['get'])
    def cluster_details(self, request, pk=None):
        k = try_int(self.request.GET.get('k'), -1)
        cluster_id = try_int(self.request.GET.get('cluster_id'), -1)
        if k == -1:
            raise NotAcceptable('`k` parameter required')
        if cluster_id == -1:
            raise NotAcceptable('`cluster_id` parameter required')
        object = self.get_object()
        return Response(object.get_cluster_members(k, cluster_id))

    def get_serializer_class(self):
        return serializers.AnalysisSerializer

    def get_queryset(self):
        query = owner_or_public(self.request.user)
        return models.Analysis.objects.filter(query)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class FeatureListCountMatrixViewset(AnalysisObjectMixin, viewsets.ReadOnlyModelViewSet):

    @detail_route(methods=['get'], renderer_classes=(PlainTextRenderer,))
    def plot(self, request, pk=None):
        object = self.get_object()
        return Response(object.get_dataset())

    @detail_route(methods=['get'])
    def sorted_render(self, request, pk=None):
        dim_x = try_int(self.request.GET.get('dim_x'))
        dim_y = try_int(self.request.GET.get('dim_y'))
        analysis_sort = (self.request.GET.get('analysis_sort') == '1')
        analysis_id = try_int(self.request.GET.get('analysis_id'))
        sort_matrix_id = self.request.GET.get('sort_id')
        if (self.request.GET.get('sort_id') == '0'):
            sort_matrix_id = None

        if any(filter(is_none, [dim_x, dim_y, analysis_id])):
            raise NotAcceptable('`dim_x`, `dim_y`, and `analysis_id` are required parameters')

        object = self.get_object()
        return Response(object.get_sorted_data(
            dim_x, dim_y, analysis_sort, sort_matrix_id, analysis_id
        ))

    def get_serializer_class(self):
        return serializers.FeatureListCountMatrixSerializer

    def get_queryset(self):
        return models.FeatureListCountMatrix.objects.all()
