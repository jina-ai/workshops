#!/usr/bin/env python
# coding: utf-8

# # Jina Workshop @ EuroPython: Building a Neural Image Search Engine

# In this workshop we will build a neural search engine for images of Pokemons.

# # Downloading data and model
# 
# Skip this if you've already downloaded them.
# 
# ## Download and Extract Data
# 
# For this example we're using Pokemon sprites from [veekun.com](https://veekun.com/dex/downloads). To download them run:
# 
# ```sh
# sh ./get_data.sh
# ```
# 
# ## Download and Extract Pretrained Model
# 
# In this example we use [BiT (Big Transfer) model](https://github.com/google-research/big_transfer), To download it:
# 
# ```sh
# sh ./download.sh
# ```

# # The problem
# 
# We want to search Pokemon by pictures! For example 
# 
# ![1.png](attachment:07a57670-02d0-4b37-89d4-e40fa91fe617.png)
# 
# May return
# 
# ![2.png](attachment:4fdcaf41-1adb-4eef-9770-94a112369dfe.png) ![3.png](attachment:dd9fe45f-6be4-4822-ae92-2d281b56c0ff.png)

# # Code

# Required imports

# In[1]:
import glob

from jina.types.document.generators import from_files

import os
import sys
from shutil import rmtree

import numpy as np

from jina import Flow, DocumentArray, Document

from jinahub.image.normalizer import ImageNormalizer
from jinahub.image.encoder.big_transfer import BigTransferEncoder


# Some configuration options.
# 
# - restrict the nr of docs we index
# - the path to the images

# In[14]:


num_docs = int(os.environ.get('JINA_MAX_DOCS', 10))
image_src = 'data/**/*.png'


# Environment variables
# 
# - workspace (folder where the encoded data will be stored)
# - port we will listen on

# In[15]:


workspace = './workspace'
os.environ['JINA_WORKSPACE'] = workspace
os.environ['JINA_PORT'] = os.environ.get('JINA_PORT', str(45678))


# We need to make sure to not index on top of an existing workspace. 
# 
# This can cause problems if you are using different configuration options between the two runs.

# In[16]:


if os.path.exists(workspace):
    print(f'Workspace at {workspace} exists. Will delete')
    rmtree(workspace)


# # Flows

# The Flow is the main pipeline in Jina. It describes the way data should be loaded, processed, stored etc. within the system. 
# 
# It is made up of components (called Executors), which are the ones doing the specific task.
# 
# Ex. we have an Encoder Executor, which loads the model and *encodes* that data; crafter Executor, which preprocesses the data; Indexer Executor, which stores and retrieves the data etc.

# ## Index Flow
# 
# Depending on your need the Flow can be configured in different ways. 
# 
# While indexing (storing) data, we can optimize the pipeline to process the data in parallel

# In[33]:


f = Flow.load_config('flows/index.yml')


# In[34]:


f.plot('index.png')


# The Flow is a context manager (like a file handler).
# 
# We load data into the pipeline from the directory we provided above. 
# 
# `request_size` dictates how many images should be sent in one request (~batching).

# In[19]:

docs = DocumentArray()

for file in glob.glob(image_src, recursive=True):
    doc = Document(uri=file)
    doc.convert_image_uri_to_blob()
    docs.append(doc)
    if len(docs) == num_docs:
        break

# docs = DocumentArray(from_files(image_src, size=num_docs, read_mode='rb'))
# for d in docs:
#     d.mime_type = 'image/png'
#     d.convert_buffer_to_blob(dtype=np.float32)


# In[22]:


docs[-1].content


# In[40]:


from jina import Executor, requests
from jina.logging.logger import JinaLogger


# In[41]:


class MyLogger(Executor):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.logger = JinaLogger('MyLogger')
    
    @requests
    def log(self, docs, **kwargs):
        self.logger.warning(len(docs))


# In[46]:


docs[0].content


# In[42]:


with f:
    return_docs = f.post(
        on='/index',
        inputs=docs,
        request_size=64,
        return_results=True
    )
    for d in return_docs[0].docs:
        assert d.embedding is not None


# # Searching

# When searching we need to make sure the data is processed in serial manner.

# In[ ]:


f = Flow.load_config('flows/query.yml')


# In[ ]:


f.plot('search.png')
