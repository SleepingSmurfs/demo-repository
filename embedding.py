from sentence_transformers import SentenceTransformer
from text_data_prepare import prepare_data
import pandas as pd
import os


class EmbeddingModel:
    def __init__(self, dir_path: str):
        self.embedding_model = SentenceTransformer(
            model_name_or_path="all-mpnet-base-v2",
            device="cpu"
        )
        print("model created")
        self.prepared_chunks = prepare_data(dir_path)

    def get_embedding(self):
        for item in self.prepared_chunks:
            item["embedding"] = self.embedding_model.encode(
                item["sentence_chunk"],
                batch_size=32,
            )
        print("data embedded")

    def save_embedding(self, dir_path: str):
        text_chunks_and_embeddings_df = pd.DataFrame(self.prepared_chunks)
        print("data to DataFrame")
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)

        embeddings_df_save_path = f"{dir_path}/chunks_and_embeddings_df.csv"
        text_chunks_and_embeddings_df.to_csv(embeddings_df_save_path,
                                             index=False)

        print("data saved")
current_file_path = os.path.abspath(__file__)
current_dir = os.path.dirname(current_file_path)

def embedding_pipeline(dir):
    embedding = EmbeddingModel(dir)
    embedding.get_embedding()
    embedding.save_embedding(f"{current_dir}/embeddings/")
