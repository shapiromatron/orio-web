#!/usr/bin/env python

import click
import numpy
from scipy import stats
from scipy.cluster.hierarchy import linkage, dendrogram, fclusterdata
from scipy.cluster.vq import kmeans2, whiten
from scipy.spatial.distance import squareform, pdist
import os
import json

class ClusterFeatures():

    def __init__(self, matrix_list):

        self.matrix_list = matrix_list
        self.execute()

    def readMatrixFilesIntoVectorMatrix(self):
        self.headers = None
        self.row_names = []
        self.vector_matrix = None

        for entry in self.matrix_list:
            matrix_fn = entry[2]
            with open(matrix_fn) as f:
                # DEAL WITH HEADERS
                # IF EMPTY, POPULATE HEADERS
                if not self.headers:
                    self.headers = next(f).strip().split()
                # ELSE, CHECK IF CONSISTENT
                else:
                    if self.headers != next(f).strip().split():
                        raise ValueError('Headers not consistent across matrices')

                # POPULATE TEMPORARY MATRIX
                matrix_temp = []
                for line in f:
                    matrix_temp.append(line.strip().split())

                # ADD SUM TO VECTOR MATRIX
                if not self.vector_matrix:
                    self.vector_matrix = []
                    for i, entry in enumerate(matrix_temp):
                        row_name = entry[0]
                        row_values = numpy.array(entry[1:]).astype(float)
                        self.row_names.append(row_name)
                        self.vector_matrix.append([numpy.sum(row_values)])
                else:
                    for i, entry in enumerate(matrix_temp):
                        row_name = entry[0]
                        row_values = numpy.array(entry[1:]).astype(float)
                        if row_name != self.row_names[i]:
                            raise ValueError('Row names do not match across matrices')
                        self.vector_matrix[i].append(numpy.sum(row_values))
        return self.vector_matrix, self.row_names

    def performClustering(self):
        whitened = whiten(self.vector_matrix)
        for i in range(2,11):
            centroids, labels = kmeans2(whitened, i)
            self.kmeans_results[i] = {
                'centroids': centroids.tolist(),
                'labels': labels.tolist()
                }

    def writeJson(self, fn):
        with open(fn, 'w') as f:
            json.dump({
                'kmeans_results': self.kmeans_results,
                'vector_matrix': self.vector_matrix,
                'bins': self.headers,
                'row_names': self.row_names
                }, f, separators=(",", ": "))

    def execute(self):
        self.kmeans_results = dict()

        self.readMatrixFilesIntoVectorMatrix()
        self.performClustering()

@click.command()
@click.argument('matrix_list_fn', type=str)
@click.argument('output_json', type=str)
def cli(matrix_list_fn, output_json):
    """
    Considering matrix files specified by a list, cluster features (rows) by
    vectors derived from matrix content

    \b
    Arguments:
    - matrix_list_fn:   List of matrix files to be considered in analysis. Each
                        row in the list corresponds to a matrix to be considered
                        in the analysis. The list contains three columns:
                            1) unique integer ID for matrix
                            2) unique name for each matrix
                            3) absolute path to matrix file
    - output_json:      Filename of output JSON
    """

    assert os.path.exists(matrix_list_fn)
    with open(matrix_list_fn) as f:
        matrix_list = [
            line.strip().split()
            for line in f.readlines()
        ]

    cf = ClusterFeatures(matrix_list)
    cf.writeJson(output_json)

if __name__ == '__main__':
    cli()
