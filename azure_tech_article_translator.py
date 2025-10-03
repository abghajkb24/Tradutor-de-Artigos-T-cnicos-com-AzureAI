import requests
import openai

# Configurações
AZURE_TRANSLATOR_KEY = "SUA_CHAVE_TRANSLATOR"
AZURE_TRANSLATOR_ENDPOINT = "https://api.cognitive.microsofttranslator.com"
AZURE_LOCATION = "sua-regiao"
OPENAI_API_KEY = "SUA_CHAVE_OPENAI"

def traduzir_azure(texto, idioma_destino):
    path = '/translate?api-version=3.0'
    params = f"&to={idioma_destino}"
    constructed_url = AZURE_TRANSLATOR_ENDPOINT + path + params
    headers = {
        'Ocp-Apim-Subscription-Key': AZURE_TRANSLATOR_KEY,
        'Ocp-Apim-Subscription-Region': AZURE_LOCATION,
        'Content-type': 'application/json'
    }
    body = [{'text': texto}]
    response = requests.post(constructed_url, headers=headers, json=body)
    response.raise_for_status()
    return response.json()[0]['translations'][0]['text']

def refinar_com_openai(texto_traduzido, texto_original, idioma_destino):
    openai.api_key = OPENAI_API_KEY

    prompt = (
        f"Você é um tradutor especializado em textos técnicos. "
        f"Revise a tradução abaixo, ajustando termos técnicos conforme o contexto. "
        f"\n\nTexto original: {texto_original} \n\nTradução automática: {texto_traduzido} "
        f"\n\nTradução refinada ({idioma_destino}):"
    )
    resposta = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=2048,
        temperature=0.2,
    )
    return resposta.choices[0].message.content.strip()

# Exemplo de uso
if __name__ == "__main__":
    texto = "A rede neural convolucional é fundamental para reconhecimento de imagens médicas."
    idioma_destino = "en"
    traducao_inicial = traduzir_azure(texto, idioma_destino)
    traducao_final = refinar_com_openai(traducao_inicial, texto, "inglês")
    print("Tradução final:", traducao_final)