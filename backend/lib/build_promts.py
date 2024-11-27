from datetime import datetime
from typing import Optional
from typing import Any, List, Dict, Union

class Tables:
    def __init__(self, name: str):
        self.name = name

def build_base_prompt(prompt: str, profile_context: str, workspace_instructions: str, assistant: Optional[Tables]) -> str:
    full_prompt = ""

    if assistant:
        full_prompt += f"<INJECT ROLE>\nYou are not an AI. You are {assistant.name}.\n</INJECT ROLE>\n\n"

    full_prompt += f"Today is {datetime.now().date()}.\n\n"

    if profile_context:
        full_prompt += f"User  Info:\n{profile_context}\n\n"

    if workspace_instructions:
        full_prompt += f"System Instructions:\n{workspace_instructions}\n\n"

    full_prompt += f"User  Instructions:\n{prompt}"

    return full_prompt
from typing import List, Optional

class Tables:
    def __init__(self, name: str):
        self.name = name

class Message:
    def __init__(self, content: str, role: str, image_paths: List[str]):
        self.content = content
        self.role = role
        self.image_paths = image_paths

class ChatPayload:
    def __init__(self, chatSettings, workspaceInstructions, chatMessages, assistant, messageFileItems, chatFileItems):
        self.chatSettings = chatSettings
        self.workspaceInstructions = workspaceInstructions
        self.chatMessages = chatMessages
        self.assistant = assistant
        self.messageFileItems = messageFileItems
        self.chatFileItems = chatFileItems

class MessageImage:
    def __init__(self, path: str, base64: str):
        self.path = path
        self.base64 = base64

def encode(text: str) -> List[int]:
    # Функция для кодирования текста в токены
    return [ord(c) for c in text]  # Пример простого кодирования

def buildRetrievalText(fileItems: List[Tables]) -> str:
    # Реализуйте вашу логику для построения текста извлечения
    return "Retrieval text based on file items."

def build_final_messages(payload: ChatPayload, profile: Tables, chatImages: List[MessageImage]) -> List[dict]:
    chatSettings = payload.chatSettings
    workspaceInstructions = payload.workspaceInstructions
    chatMessages = payload.chatMessages
    assistant = payload.assistant
    messageFileItems = payload.messageFileItems
    chatFileItems = payload.chatFileItems

    BUILT_PROMPT = build_base_prompt(
        chatSettings.prompt,
        chatSettings.includeProfileContext and profile.profile_context or "",
        chatSettings.includeWorkspaceInstructions and workspaceInstructions or "",
        assistant
    )

    CHUNK_SIZE = chatSettings.contextLength
    PROMPT_TOKENS = len(encode(chatSettings.prompt))

    remaining_tokens = CHUNK_SIZE - PROMPT_TOKENS
    used_tokens = PROMPT_TOKENS

    processed_chat_messages = []

    for index, chatMessage in enumerate(chatMessages):
        next_chat_message = chatMessages[index + 1] if index + 1 < len(chatMessages) else None

        if next_chat_message:
            next_chat_message_file_items = next_chat_message.fileItems

            if next_chat_message_file_items:
                find_file_items = [
                    chatFileItem for fileItemId in next_chat_message_file_items
                    for chatFileItem in chatFileItems if chatFileItem.id == fileItemId
                ]

                retrieval_text = buildRetrievalText(find_file_items)

                processed_chat_messages.append({
                    'message': {
                        **chatMessage.message,
                        'content': f"{chatMessage.message.content}\n\n{retrieval_text}"
                    },
                    'fileItems': []
                })
            else:
                processed_chat_messages.append(chatMessage)
        else:
            processed_chat_messages.append(chatMessage)

    final_messages = []

    for message in reversed(processed_chat_messages):
        message_content = message['message']['content']
        message_tokens = len(encode(message_content))

        if message_tokens <= remaining_tokens:
            remaining_tokens -= message_tokens
            used_tokens += message_tokens
            final_messages.insert(0, message['message'])
        else:
            break

    temp_system_message = {
        'chat_id': "",
        'assistant_id': None,
        'content': BUILT_PROMPT,
        'created_at': "",
        'id': str(len(processed_chat_messages)),
        'image_paths': [],
        'model': chatSettings.model,
        'role': "system",
        'sequence_number': len(processed_chat_messages),
        'updated_at': "",
        'user_id': ""
    }

    final_messages.insert(0, temp_system_message)

    final_messages = [
        {
            'role': message['role'],
            'content': [
                {'type': 'text', 'text': message['content']}
            ] + [
                {'type': 'image_url', 'image_url': {'url': (chatImage.base64 if (chatImage := next((img for img in chatImages if img.path == path), None)) else path)}}
                 for path in message['image_paths']
            ] if message['image_paths'] else message['content']
        }
        for message in final_messages
    ]

    if messageFileItems:
        retrieval_text = buildRetrievalText(messageFileItems)
        final_messages[-1]['content'] = f"{final_messages[-1]['content']}\n\n{retrieval_text}"

    return final_messages

class Tables:
    def __init__(self, name: str, content: str):
        self.name = name
        self.content = content

def build_retrieval_text(file_items: List[Tables]) -> str:
    retrieval_text = "\n\n".join(f"<BEGIN SOURCE>\n{item.content}\n</END SOURCE>" for item in file_items)

    return f"You may use the following sources if needed to answer the user's question. If you don't know the answer, say 'I don't know.'\n\n{retrieval_text}"


def get_base64_from_data_url(data_url: str) -> str:
    # Здесь должна быть реализация для извлечения base64 из data URL
    pass

def get_media_type_from_data_url(data_url: str) -> str:
    # Здесь должна быть реализация для извлечения типа медиа из data URL
    pass

def adapt_single_message_for_google_gemini(message: Dict[str, Any]) -> Dict[str, Any]:
    adapted_parts = []
    raw_parts = []

    if not isinstance(message.get('content'), list):
        raw_parts.append({'type': 'text', 'text': message.get('content')})
    else:
        raw_parts = message.get('content')

    for raw_part in raw_parts:
        if raw_part.get('type') == 'text':
            adapted_parts.append({'text': raw_part.get('text')})
        elif raw_part.get('type') == 'image_url':
            adapted_parts.append({
                'inlineData': {
                    'data': get_base64_from_data_url(raw_part.get('image_url').get('url')),
                    'mimeType': get_media_type_from_data_url(raw_part.get('image_url').get('url')),
                }
            })

    role = 'user'
    if message.get('role') in ['user', 'system']:
        role = 'user'
    elif message.get('role') == 'assistant':
        role = 'model'

    return {
        'role': role,
        'parts': adapted_parts
    }
def adapt_messages_for_gemini_vision(messages):
    # Gemini Pro Vision cannot process multiple messages
    # Reformat, using all texts and last visual only

    base_prompt = messages[0]['parts'][0]['text']
    base_role = messages[0]['role']
    last_message = messages[-1]
    visual_message_parts = last_message['parts']
    
    visual_query_messages = [{
        'role': 'user',
        'parts': [
            f"{base_role}:\n{base_prompt}\n\nuser:\n{visual_message_parts[0]['text']}\n\n",
            visual_message_parts[1:]
        ]
    }]
    
    return visual_query_messages

async def adapt_messages_for_google_gemini(payload, messages):
    gemini_messages = []
    for message in messages:
        adapted_message = adapt_single_message_for_google_gemini(message)
        gemini_messages.append(adapted_message)

    if payload['chatSettings']['model'] == "gemini-pro-vision":
        gemini_messages = adapt_messages_for_gemini_vision(gemini_messages)
    
    return gemini_messages


