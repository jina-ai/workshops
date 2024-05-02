from typing import Dict, Tuple
import os
import time

import numpy as np

from jina import Executor, DocumentArray, requests, Document
from jina.types.arrays.memmap import DocumentArrayMemmap
from jina.logging.logger import JinaLogger


class RequestLogger(Executor):                                                                      # needs to inherit from Executor
    def __init__(self,
                default_log_docs: int = 1,                                                          # your arguments
                *args, **kwargs):                                                                   # *args and **kwargs are required for Executor
        super().__init__(*args, **kwargs)                                                           # before any custom logic
        self.default_log_docs = default_log_docs
        self.logger = JinaLogger('req_logger')
        self.log_path = os.path.join(self.workspace, 'log.txt')
        if not os.path.exists(self.log_path):
            with open(self.log_path, 'w'): pass

    @requests                                                                                       # decorate, by default it will be called on every request
    def log(self,                                                                                   # arguments are automatically received
            docs: DocumentArray,
            parameters: Dict,
            **kwargs):
        self.logger.info('Request being processed...')

        nr_docs = int(parameters.get('log_docs', self.default_log_docs))                            # accesing parameters (nr are passed as float due to Protobuf)
        with open(self.log_path, 'a') as f:
            f.write(f'request at time {time.time()} with {len(docs)} documents:\n')
            for i, doc in enumerate(docs):
                f.write(f'\tprocessing doc.id {doc.id}. content = {doc.content}\n')
                if i + 1 == nr_docs:
                    break



class MemMapIndexer(Executor):
    def __init__(self, index_file_name: str, **kwargs):
        super().__init__(**kwargs)
        self._docs = DocumentArrayMemmap(self.workspace + f'/{index_file_name}')

    @requests(on='/index')
    def index(self, docs: 'DocumentArray', **kwargs):
        self._docs.extend(docs)

    @requests(on='/search')
    def search(self, docs: 'DocumentArray', parameters: Dict, **kwargs):
        a = np.stack(docs.get_attributes('embedding'))
        b = np.stack(self._docs.get_attributes('embedding'))
        q_emb = _ext_A(_norm(a))
        d_emb = _ext_B(_norm(b))
        dists = _cosine(q_emb, d_emb)
        idx, dist = self._get_sorted_top_k(dists, int(parameters.get('top_k', 5)))
        for _q, _ids, _dists in zip(docs, idx, dist):
            for _id, _dist in zip(_ids, _dists):
                d = Document(self._docs[int(_id)], copy=True)
                d.scores['cosine'] = 1 - _dist
                _q.matches.append(d)

    @staticmethod
    def _get_sorted_top_k(
        dist: 'np.array', top_k: int
    ) -> Tuple['np.ndarray', 'np.ndarray']:
        if top_k >= dist.shape[1]:
            idx = dist.argsort(axis=1)[:, :top_k]
            dist = np.take_along_axis(dist, idx, axis=1)
        else:
            idx_ps = dist.argpartition(kth=top_k, axis=1)[:, :top_k]
            dist = np.take_along_axis(dist, idx_ps, axis=1)
            idx_fs = dist.argsort(axis=1)
            idx = np.take_along_axis(idx_ps, idx_fs, axis=1)
            dist = np.take_along_axis(dist, idx_fs, axis=1)

        return idx, dist


def _get_ones(x, y):
    return np.ones((x, y))


def _ext_A(A):
    nA, dim = A.shape
    A_ext = _get_ones(nA, dim * 3)
    A_ext[:, dim : 2 * dim] = A
    A_ext[:, 2 * dim :] = A ** 2
    return A_ext


def _ext_B(B):
    nB, dim = B.shape
    B_ext = _get_ones(dim * 3, nB)
    B_ext[:dim] = (B ** 2).T
    B_ext[dim : 2 * dim] = -2.0 * B.T
    del B
    return B_ext


def _euclidean(A_ext, B_ext):
    sqdist = A_ext.dot(B_ext).clip(min=0)
    return np.sqrt(sqdist)


def _norm(A):
    return A / np.linalg.norm(A, ord=2, axis=1, keepdims=True)


def _cosine(A_norm_ext, B_norm_ext):
    return A_norm_ext.dot(B_norm_ext).clip(min=0) / 2


class RequestLogger(Executor):                                                                      # needs to inherit from Executor
    def __init__(self,
                default_log_docs: int = 1,                                                          # your arguments
                *args, **kwargs):                                                                   # *args and **kwargs are required for Executor
        super().__init__(*args, **kwargs)                                                           # before any custom logic
        self.default_log_docs = default_log_docs
        self.logger = JinaLogger('req_logger')
        self.log_path = os.path.join(self.workspace, 'log.txt')
        if not os.path.exists(self.log_path):
            with open(self.log_path, 'w'): pass

    @requests                                                                                       # decorate, by default it will be called on every request
    def log(self,                                                                                   # arguments are automatically received
            docs: DocumentArray,
            parameters: Dict,
            **kwargs):
        self.logger.info('Request being processed...')

        nr_docs = int(parameters.get('log_docs', self.default_log_docs))                            # accesing parameters (nr are passed as float due to Protobuf)
        with open(self.log_path, 'a') as f:
            f.write(f'request at time {time.time()} with {len(docs)} documents:\n')
            for i, doc in enumerate(docs):
                f.write(f'\tsearching with doc.id {doc.id}. filename = {doc.tags["filename"]}\n')
                if i + 1 == nr_docs:
                    break
