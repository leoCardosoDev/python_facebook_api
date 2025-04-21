import os
import requests
from dotenv import load_dotenv

# Carrega variáveis de ambiente do arquivo .env
load_dotenv()
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
IG_USER_ID = os.getenv("IG_USER_ID")

def upload_image(image_url, caption):
    """
    Realiza o upload da imagem para o Instagram via Graph API.
    Args:
        image_url (str): URL pública da imagem.
        caption (str): Legenda da publicação.
    Returns:
        str: ID da criação do media (creation_id) para publicação posterior.
    Raises:
        Exception: Se houver erro na requisição ou no parsing da resposta.
    """
    upload_url = f"https://graph.facebook.com/v22.0/{IG_USER_ID}/media"
    payload = {
        'image_url': image_url,   # A URL DEVE ser acessível publicamente!
        'caption': caption,
        'access_token': ACCESS_TOKEN
    }
    try:
        res = requests.post(upload_url, data=payload, timeout=30)
        print("Status:", res.status_code)
        print("Resposta bruta da API:", res.text)
        res.raise_for_status()  # Gera erro para HTTP status 4xx/5xx
        response_json = res.json()
        if 'id' not in response_json:
            raise Exception(f"Upload não retornou ID de criação. Resposta: {response_json}")
        return response_json['id']
    except requests.exceptions.RequestException as req_err:
        # Erro de rede, URL inválida, timeout, etc.
        raise Exception(f"Erro de conexão no upload: {req_err}")
    except Exception as e:
        raise Exception(f"Erro na resposta do upload: {e}")

def publish_image(creation_id):
    """
    Publica a imagem no Instagram após o upload.
    Args:
        creation_id (str): ID de criação da mídia obtido na etapa de upload.
    Returns:
        dict: Resposta completa da API.
    Raises:
        Exception: Se houver erro na requisição ou no parsing da resposta.
    """
    publish_url = f"https://graph.facebook.com/v22.0/{IG_USER_ID}/media_publish"
    payload = {
        'creation_id': creation_id,
        'access_token': ACCESS_TOKEN
    }
    try:
        res = requests.post(publish_url, data=payload, timeout=30)
        # Gera erro para HTTP status 4xx/5xx    
        res.raise_for_status()
        response_json = res.json()
        if 'id' not in response_json:
            raise Exception(f"Publicação não retornou ID. Resposta: {response_json}")
        return response_json
    except requests.exceptions.RequestException as req_err:
        raise Exception(f"Erro de conexão na publicação: {req_err}")
    except Exception as e:
        raise Exception(f"Erro na resposta da publicação: {e}")

def main():
    # Coleta os parâmetros
    IMG_DIR = "img"
    caption = "Publicação automática via Python & Graph API! 🚀"

    # IMPORTANTE! Hospede esta imagem e obtenha a URL pública de acesso direto
    image_url = "https://i.imgur.com/R2GMxHN.png"  # Exemplo: https://meu-bucket.s3.amazonaws.com/minha_imagem.jpg

    print("Iniciando upload da imagem para o Instagram...")

    try:
        creation_id = upload_image(image_url, caption)
        print(f"Upload concluído. creation_id: {creation_id}")

        print("Publicando imagem no perfil...")
        result = publish_image(creation_id)
        print("Publicação realizada com sucesso!")
        print("Dados retornados:", result)
    except Exception as e:
        print(f"Erro no processo: {e}")
        print("Recomendações:")
        print("- Verifique se o ACCESS_TOKEN e IG_USER_ID estão corretos e válidos.")
        print("- A imagem precisa estar hospedada em URL pública acessível (erros frequentes com URL inválida).")
        print("- Confirme as permissões do Facebook App (modo live, permissões 'instagram_basic', etc).")
        print("- Consulte o log de erro acima para detalhes.")

if __name__ == "__main__":
    main()