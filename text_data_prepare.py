import glob
import re

from spacy.lang.ru import Russian

num_sentence_chunk_size = 10
min_token_length = 30


# keys: text: str, token_count: float
def read_data(dir_path: str, data: list[dict]) -> None:
    for file_path in glob.iglob(f'{dir_path}*.txt'):
        with open(file_path, 'r') as file:
            page_data = dict()
            page_data['text'] = file.read().replace('\n', ' ').strip()
            page_data['token_count'] = len(page_data['text']) / 4
            data.append(page_data)


# keys: text: str, token_count: float, sentences: list[str]
# page_sentence_count_spacy: int
def break_into_sentences(data: list[dict]) -> None:
    nlp = Russian()
    nlp.add_pipe("sentencizer")

    for item in data:
        item["sentences"] = list(nlp(item["text"]).sents)
        item["sentences"] = [str(sentence) for sentence in item["sentences"]]
        item["page_sentence_count_spacy"] = len(item["sentences"])


def split_list(input_list: list, slice_size: int) -> list[list[str]]:
    return [input_list[i:i + slice_size] for i in
            range(0, len(input_list), slice_size)]


# keys: text: str, token_count: float, sentences: list[str]
# page_sentence_count_spacy: int, sentence_chunks: list[list[str]]
# num_chunks: int
def break_into_chunks(data: list[dict]) -> None:
    for item in data:
        item["sentence_chunks"] = split_list(input_list=item["sentences"],
                                             slice_size=num_sentence_chunk_size)
        item["num_chunks"] = len(item["sentence_chunks"])


# keys: number: int, sentence_chunk: str,
# chunk_char_count: int, chunk_word_count: 59,
# chunk_token_count: float
def join_chunks_from_all_data(data: list[dict], chunks: list[dict]) -> None:
    for item in data:
        for i, sentence_chunk in enumerate(item["sentence_chunks"]):
            chunk_dict = dict()
            chunk_dict["number"] = i

            joined_sentence_chunk = "".join(sentence_chunk).replace("  ",
                                                                    " ").strip()
            joined_sentence_chunk = re.sub(r'\.([A-Z])', r'. \1',
                                           joined_sentence_chunk)
            chunk_dict["sentence_chunk"] = joined_sentence_chunk

            chunk_dict["chunk_char_count"] = len(joined_sentence_chunk)
            chunk_dict["chunk_word_count"] = len(
                [word for word in joined_sentence_chunk.split(" ")])
            chunk_dict["chunk_token_count"] = len(
                joined_sentence_chunk) / 4

            chunks.append(chunk_dict)


def filter_small_chunks(chunks: list[dict]):
    for item in chunks:
        if item["chunk_token_count"] < min_token_length:
            del chunks[chunks.index(item)]


def prepare_data(dir_path: str):
    data = []
    read_data(dir_path, data)
    break_into_sentences(data)
    break_into_chunks(data)

    chunks = []
    join_chunks_from_all_data(data, chunks)
    filter_small_chunks(chunks)

    print("data prepared")

    return chunks

# keys: number: int, sentence_chunk: str,
# chunk_char_count: int, chunk_word_count: 59,
# chunk_token_count: float
