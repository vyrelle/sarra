# backend/src/infrastructure/services/huggingface/query_transformation_service.py
from openai import OpenAI
import os
from ....application.services.query_transformation_service import IQueryTransformationService

class HfQueryTransformationService(IQueryTransformationService):
    def __init__(self):
        self.hf_client = OpenAI(
            base_url="https://router.huggingface.co/v1",
            api_key=os.getenv("HF_TOKEN")
        )
        # Используем более легкую и быструю модель специально для этой задачи
        self.model = "meta-llama/Llama-3.1-8B-Instruct"

    async def generate_hypothetical_answer(self, query: str) -> str:
        prompt = f"""You are an expert in the public services of Kazakhstan. Create a concise, factual, hypothetical answer to the user's question. The goal is to generate keywords and context for a better search.

Question: {query}

Answer:"""

        try:
            response = await self.hf_client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a search query enhancement expert."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=200,
                temperature=0.2
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            print(f"Query transformation failed: {e}")
            # В случае ошибки, возвращаем исходный запрос, чтобы не прерывать пайплайн
            return query
