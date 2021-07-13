import os
import time
from typing import Dict

from jina import Executor, DocumentArray, requests


class RequestLogger(Executor):                                                                      # needs to inherit from Executor
    def __init__(self,
                default_log_docs: int = 1,                                                          # your arguments
                *args, **kwargs):                                                                   # *args and **kwargs are required for Executor
        super().__init__(*args, **kwargs)                                                           # before any custom logic
        self.default_log_docs = default_log_docs
        self.log_path = os.path.join(self.workspace, 'log.txt')
        if not os.path.exists(self.log_path):
            with open(self.log_path, 'w'): pass

    @requests                                                                                       # decorate, by default it will be called on every request
    def log(self,                                                                                   # arguments are automatically received
            docs: DocumentArray,
            parameters: Dict,
            **kwargs):
        nr_docs = int(parameters.get('log_docs', self.default_log_docs))                            # accesing parameters (nr are passed as float due to Protobuf)
        with open(self.log_path, 'a') as f:
            f.write(f'request at time {time.time()} with {len(docs)} documents:\n')
            for i, doc in enumerate(docs):
                f.write(f'\tsearching with doc.id {doc.id}. content = {doc.content}\n')
                if i + 1 == nr_docs:
                    break
