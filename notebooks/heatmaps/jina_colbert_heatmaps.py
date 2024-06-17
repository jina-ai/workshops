import matplotlib.pyplot as plt
import requests
import seaborn
import string
import torch
import torch.nn.functional as F

from colbert.modeling.checkpoint import Checkpoint
from colbert.infra import ColBERTConfig
from matplotlib.patches import Rectangle
from transformers import AutoTokenizer


def preprocess_doc(doc):
    embeddings = [torch.Tensor(doc["embeddings"])]
    max_length = max(embd.size() for embd in embeddings)[0]

    padded_embeddings = [
        F.pad(embd, (0, 0, 0, max_length - embd.size()[0]), "constant", 0)
        for embd in embeddings
    ]
    return torch.stack(padded_embeddings)


def compute_relevance_scores_colbert(query_embeddings, document_embeddings):
    """
    Compute relevance scores for top-k documents given a query.

    :param query_embeddings: Tensor representing the query embeddings, shape: [num_query_terms, embedding_dim]
    :param document_embeddings: Tensor representing embeddings for k documents, shape: [k, max_doc_length, embedding_dim]
    :param k: Number of top documents to re-rank
    :return: Sorted document indices based on their relevance scores
    """

    # Ensure document_embeddings is a 3D tensor: [k, max_doc_length, embedding_dim]
    # Pad the k documents to their maximum length for batch operations
    # Note: Assuming document_embeddings is already padded and moved to GPU

    # Compute batch dot-product of Eq (query embeddings) and D (document embeddings)
    # Resulting shape: [k, num_query_terms, max_doc_length]

    scores = torch.matmul(
        query_embeddings.unsqueeze(0), document_embeddings.transpose(1, 2)
    )

    # Apply max-pooling across document terms (dim=2) to find the max similarity per query term
    # Shape after max-pool: [k, num_query_terms]
    max_scores_per_query_term = scores.max(dim=2).values

    # Sum the scores across query terms to get the total score for each document
    # Shape after sum: [k]
    total_scores = max_scores_per_query_term.sum(dim=1)

    # Sort the documents based on their total scores
    sorted_indices = total_scores.argsort(descending=True)

    return sorted_indices, scores


def create_single_heatmap(scores, query_tokens, document_tokens):
    fig, axs = plt.subplots(nrows=1, ncols=1)
    seaborn.set_theme(rc={"figure.figsize": (20, 7)})
    fig.subplots_adjust(bottom=0.2, top=0.95, right=0.95)
    s_plot = seaborn.heatmap(
        scores[:, : len(document_tokens)],
        ax=axs,
        cbar=True,
        vmin=-0.5,
        vmax=1,
        xticklabels=document_tokens,
        yticklabels=query_tokens,
    )
    if not True:
        axs.axis("off")
    if True:
        for index in range(scores.size()[0]):
            position = scores[index].argmax()

            s_plot.add_patch(
                Rectangle(
                    (position, index), 1, 1, fill=False, edgecolor="red", lw=3
                )
            )
    #plt.close()
    return fig


def filter_query_tokens(tokens):
    return list(filter(lambda x: x not in string.punctuation, tokens))


class JinaColbertHeatmapMaker:
    def __init__(self, jina_api_key: str):
        self.auto_tokenizer = AutoTokenizer.from_pretrained("jinaai/jina-colbert-v1-en")
        ckpt = Checkpoint(
            "jinaai/jina-colbert-v1-en",
            colbert_config=ColBERTConfig(root="experiments"),
        )
        self.query_tokenizer = ckpt.query_tokenizer
        self.doc_tokenizer = ckpt.doc_tokenizer
        self.jina_api_key = jina_api_key

    def tokenize(self, text, is_query=True):
        auto_tokens = self.auto_tokenizer.tokenize(
            text,
            padding=False,
            truncation=True,
            return_token_type_ids=False,
        )
        if is_query:
            all_encoded_inputs = self.query_tokenizer.tok(
                [text],
                padding=False,
                truncation=True,
                return_token_type_ids=False,
            )
        else:
            all_encoded_inputs = self.doc_tokenizer.tok(
                [text],
                padding=False,
                truncation=True,
                return_token_type_ids=False,
            )

        string_token = self.auto_tokenizer.convert_ids_to_tokens(
            all_encoded_inputs["input_ids"][0]
        )
        if not is_query:
            string_token = filter_query_tokens(string_token)
            auto_tokens = filter_query_tokens(auto_tokens)
        if len(string_token) != len(auto_tokens) + 2:
            print("Wrong token count:", len(string_token), len(auto_tokens))

        return string_token

    def compute_heatmap(self, document, query):
        document_embeddings = preprocess_doc(document)

        query_embeddings = torch.Tensor(query["embeddings"])
        sorted_indices, scores = compute_relevance_scores_colbert(
            query_embeddings, document_embeddings
        )
        query_tokens = self.tokenize(query["text"], is_query=True)
        document_tokens = self.tokenize(
            document["text"], is_query=False
        )
        return create_single_heatmap(scores[0], query_tokens, document_tokens)

    def embed(self, text: str, is_query: bool = True):
        if is_query:
            input_type = "query"
        else:
            input_type = "document"
        trimmed_text = text[:10000]
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.jina_api_key}",
        }
        data = {
            "input": trimmed_text,
            "model": "jina-colbert-v1-en",
            "input_type": input_type,
        }
        response = requests.post(
            url="https://api.jina.ai/v1/multi-embeddings", headers=headers, json=data
        )
        if response.status_code == 200:
            embeddings = response.json()["data"]
            if embeddings:
                embedded_docs = [{"text": text, "embeddings": embeddings[0]["embeddings"]}]
            return embedded_docs
        else:
            print("ERROR: No results")
            print(response.status_code)
            print(response)
            return [{"text": text}]
