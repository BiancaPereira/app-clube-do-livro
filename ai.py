import os

from google import genai

gemini_key = os.getenv('GEMINI_KEY')
client = genai.Client(api_key=gemini_key)

def generate_ai_summary(book: str) -> str:
    response = client.models.generate_content(
        model="gemini-2.0-flash", contents=f'Escreva um mini sinopse informal e chamativa sobre o livro {book} de até 2 linhas, adicionando o gênero no final entre parênteses e adiciona um emoji com uma bandeirinha do país de origem do autor.'
    )

    return response.text
