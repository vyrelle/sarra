

from typing import List, Dict
from openai import OpenAI
import os
from ....application.services.chat_service import IChatService

class ChatService(IChatService):
    def __init__(self):
        self.hf_client = OpenAI(
            base_url="https://router.huggingface.co/v1",
            api_key=os.getenv("HF_TOKEN")
        )

    async def generate_answer(self, question: str, context: List[Dict]) -> str:
        context_str = "\n\n".join([f"Source: {c['name']}\nContent: {c['content']}" for c in context])
        
        response = await self.hf_client.chat.completions.create(
            model="meta-llama/Llama-3.3-70B-Instruct",
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful assistant for Kazakhstan government services."
                },
                {
                    "role": "user",
                    "content": f"Context:\n{context_str}\n\nQuestion: {question}"
                }
            ],
            max_tokens=1024,
            temperature=0.3
        )
        return response.choices[0].message.content

