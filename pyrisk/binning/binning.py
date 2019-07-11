import pandas as pd
import numpy as np
from sklearn.cluster import AgglomerativeClustering


# TODO: move to utils folder
class NotFittedError(Exception):
    def __init__(self, message):
        self.message = message


class Bucketer(object):
    def __init__(self):
        self.fitted = False

    def fit(self, x):
        """ Create bucketing on the array x

        Args:
            x: input array

        Returns: fitted bucketer object

        """
        self._fit(x)
        self.fitted = True
        return self

    def apply_bucketing(self, x_new):
        # TODO: decide on the output of this function
        if not self.fitted:
            raise NotFittedError('Bucketer is not fitted')
        else:
            return np.digitize(x_new, self.boundaries)


class SimpleBucketer(Bucketer):
    """Create equaly spaced bins using numpy.histogram function

    Usage:
    x = [1, 2, 1]
    bins = 3
    myBucketer = SimpleBucketer(bin_count=bins)
    myBucketer.fit(x)

    myBucketer.counts gives the number of elements per bucket
    myBucketer.boundaries gives the boundaries of the buckets

    """

    def __init__(self, bin_count):
        super().__init__()
        self.bin_count = bin_count

    @staticmethod
    def simple_bins(x, bin_count):
        counts, boundaries = np.histogram(x, bins=bin_count)
        return counts, boundaries

    def _fit(self, x):
        self.counts, self.boundaries = self.simple_bins(x, self.bin_count)


class AgglomerativeBucketer(Bucketer):
    """Create binning by applying the Scikit-learn implementation of Agglomerative Clustering

    Usage:
    x = [1, 2, 1]
    bins = 3
    myBucketer = AgglomerativeBucketer(bin_count=bins)
    myBucketer.fit(x)

    myBucketer.counts gives the number of elements per bucket
    myBucketer.boundaries gives the boundaries of the buckets

    """

    def __init__(self, bin_count):
        super().__init__()
        self.bin_count = bin_count

    @staticmethod
    def agglomerative_clustering_binning(x, bin_count):
        clustering = AgglomerativeClustering(n_clusters=bin_count).fit(np.asarray(x).reshape(-1, 1))
        df = pd.DataFrame({'x': x, 'label': clustering.labels_}).sort_values(by='x')
        cluster_minimum_values = df.groupby('label')['x'].min().sort_values().tolist()
        cluster_maximum_values = df.groupby('label')['x'].max().sort_values().tolist()
        # take the mean of the upper boundary of a cluster and the lower boundary of the next cluster
        boundaries = [np.mean([cluster_minimum_values[i + 1], cluster_maximum_values[i]]) for i in
                      range(len(cluster_minimum_values) - 1)]
        # add the lower boundary of the lowest cluster and the upper boundary of the highest cluster
        boundaries = [cluster_minimum_values[0]] + boundaries + [cluster_maximum_values[-1]]
        counts = df.groupby('label')['label'].count().values
        return counts, boundaries

    def _fit(self, x):
        self.counts, self.boundaries = self.agglomerative_clustering_binning(x, self.bin_count)


class QuantileBucketer(Bucketer):
    """Create bins with equal number of elements

    Usage:
    x = [1, 2, 1]
    bins = 3
    myBucketer = QuantileBucketer(bin_count=bins)
    myBucketer.fit(x)

    myBucketer.counts gives the number of elements per bucket
    myBucketer.boundaries gives the boundaries of the buckets

    """

    def __init__(self, bin_count):
        super().__init__()
        self.bin_count = bin_count

    @staticmethod
    def quantile_bins(x, bin_count):
        out, boundaries = pd.qcut(x, q=bin_count, retbins=True)
        df = pd.DataFrame({'x': x})
        df['label'] = out
        counts = df.groupby('label').count().values.flatten()
        return counts, boundaries

    def _fit(self, x):
        self.counts, self.boundaries = self.quantile_bins(x, self.bin_count)