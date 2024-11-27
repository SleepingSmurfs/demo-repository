import base64

def convert_blob_to_base64(blob: bytes) -> str:
    return base64.b64encode(blob).decode('utf-8')

# # Пример использования
# if __name__ == "__main__":
#     # Пример байтового объекта
#     example_blob = b'This is a test blob.'
#     base64_string = convert_blob_to_base64(example_blob)
#     print(base64_string)