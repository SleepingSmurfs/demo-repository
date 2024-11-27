import random

import torch
import numpy as np
import pandas as pd

from sentence_transformers import util, SentenceTransformer

PATH_TO_EMBEDDINGS = "embeddings/chunks_and_embeddings_df.csv"
DEVICE = 'cpu'


def import_embeddings():
    global DEVICE
    DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

    text_chunks_and_embedding_df = pd.read_csv(PATH_TO_EMBEDDINGS)

    text_chunks_and_embedding_df["embedding"] = text_chunks_and_embedding_df[
        "embedding"].apply(lambda x: np.fromstring(x.strip("[]"), sep=" "))

    pages_and_chunks = text_chunks_and_embedding_df.to_dict(orient="records")

    embeddings = torch.tensor(
        np.array(text_chunks_and_embedding_df["embedding"].tolist()),
        dtype=torch.float32).to(DEVICE)

    return pages_and_chunks, embeddings


def retrieve_relevant_resources(
        query: str,
        embeddings: torch.tensor,
        model: SentenceTransformer,
        n_resources_to_return: int = 5
):
    query_embedding = model.encode(query,
                                   convert_to_tensor=True)

    dot_scores = util.dot_score(query_embedding, embeddings)[0]

    scores, indices = torch.topk(input=dot_scores,
                                 k=n_resources_to_return)

    return scores, indices
