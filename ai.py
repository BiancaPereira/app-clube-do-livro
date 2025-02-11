import os

from google import genai

gemini_key = os.getenv('GEMINI_KEY')
client = genai.Client(api_key=gemini_key)

def generate_ai_summary(resume: str, book: str, writer: str) -> str:
    response = client.models.generate_content(
        model="gemini-2.0-flash", contents=f'Resuma essa sinopse (sinopse: {resume}) do livro {book} em 1 linha chamativa. Adicione o gênero no final entre parênteses e adiciona um hífem depois com o nome do autor {writer}.'
    )

    return response.text
