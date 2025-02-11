import os

from google import genai

gemini_key = os.getenv('GEMINI_KEY')
client = genai.Client(api_key=gemini_key)

def generate_ai_summary(book: str, writer: str) -> str:
    response = client.models.generate_content(
        model="gemini-2.0-flash", contents=f'Escreva um mini sinopse sobre o livro {book} de até 1 linha. Não invente, pegue essa informação de um local confiável. Adicione o gênero no final entre parênteses e adiciona um hífem depois com o nome do autor {writer}.'
    )

    return response.text
