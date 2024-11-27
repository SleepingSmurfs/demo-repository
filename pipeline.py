from sentence_transformers import SentenceTransformer

from embedding import embedding_pipeline
from rag import import_embeddings
from llm import choose_model_based_on_gpu, config_models, ask


def input_query():
    query = "How are you?"
    return query


if __name__ == "__main__":
    action = int(input())

    # Загрузка данных
    if action == 1:
        embedding_pipeline()
    # Ответ на запрос
    else:
        pages_and_chunks, embeddings = import_embeddings()

        device = 'cpu'
        embedding_model = SentenceTransformer(
            model_name_or_path="all-mpnet-base-v2",
            device=device
        )

        use_quantization_config, model_id = choose_model_based_on_gpu()
        tokenizer, llm_model = config_models(use_quantization_config, model_id)

        query = input_query()

        output_text = ask(
            query=query,
            embeddings=embeddings,
            pages_and_chunks=pages_and_chunks,
            embedding_model=embedding_model,
            tokenizer=tokenizer,
            llm_model=llm_model,
            return_answer_only=True
        )
