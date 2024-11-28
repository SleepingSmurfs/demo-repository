import textwrap
import torch
import numpy as np
import pandas as pd
import os

from sentence_transformers import util, SentenceTransformer
current_file_path = os.path.abspath(__file__)
current_dir = os.path.dirname(current_file_path)
PATH_TO_EMBEDDINGS = f"{current_dir}/embeddings/chunks_and_embeddings_df.csv"
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


def print_wrapped(text, wrap_length=80):
    wrapped_text = textwrap.fill(text, wrap_length)
    print(wrapped_text)


def print_top_results_and_scores(
        query: str,
        embeddings: torch.tensor,
        pages_and_chunks: list[dict],
        model: SentenceTransformer,
        n_resources_to_return: int = 5
):
    scores, indices = retrieve_relevant_resources(
        query=query,
        embeddings=embeddings,
        model=model,
        n_resources_to_return=n_resources_to_return
    )

    print("Результат: ")
    for score, index in zip(scores, indices):
        print(f"Score: {score:.4f}")
        print_wrapped(pages_and_chunks[index]["sentence_chunk"])
        print(f"Номер документа: {pages_and_chunks[index]['number']}")


def create_dangerous_topic_embeddings(
        topics: list[str],
        model: SentenceTransformer
):
    return model.encode(topics, convert_to_tensor=True)


def is_dangerous_query_with_similarity(
        query: str, model: SentenceTransformer,
        dangerous_embeddings,
        threshold: float = 0.8
) -> bool:
    query_embedding = model.encode(query, convert_to_tensor=True)

    similarities = util.cos_sim(query_embedding, dangerous_embeddings)

    max_similarity = similarities.max().item()
    # print("Max similarity: ", max_similarity)
    return max_similarity > threshold
