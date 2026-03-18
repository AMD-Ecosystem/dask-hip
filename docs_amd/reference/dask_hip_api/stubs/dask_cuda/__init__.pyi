from _typeshed import Incomplete

from ._version import __git_commit__ as __git_commit__, __version__ as __version__
from .cuda_worker import CUDAWorker as CUDAWorker
from .local_cuda_cluster import LocalCUDACluster as LocalCUDACluster

DASK_USE_ROCM: Incomplete
