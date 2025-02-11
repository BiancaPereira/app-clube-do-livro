import os

from google import genai

gemini_key = os.getenv('GEMINI_KEY')
client = genai.Client(api_key=gemini_key)

def generate_ai_summary(book: str, writer: str) -> str:
    response = client.models.generate_content(
        model="gemini-2.0-flash", contents=f'Escreva um mini sinopse chamativa sobre o livro {book} de até 1 linha, adicionando o gênero no final entre parênteses e adiciona o nome do autor {writer}.'
    )

    return response.text
