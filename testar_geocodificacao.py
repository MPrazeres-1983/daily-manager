import requests


def obter_coordenadas(endereco):
    url = "https://nominatim.openstreetmap.org/search"
    params = {"q": endereco, "format": "json"}
    resposta = requests.get(
        url, params=params, headers={"User-Agent": "DailyManagerApp"}
    )
    if resposta.status_code == 200 and resposta.json():
        dados = resposta.json()[0]
        return f"{dados['lat']},{dados['lon']}"
    return ""


enderecos = [
    "Rua da escola do exército, Lisboa",
    "Rua Augusta, Lisboa",
    "Avenida da Liberdade, Lisboa",
    "Porto",
    "Praça do Comércio, Lisboa",
    "Nome inventado que não existe",
]

for endereco in enderecos:
    coordenadas = obter_coordenadas(endereco)
    print(f"Endereço: {endereco}")
    print(f"Coordenadas: {coordenadas if coordenadas else 'Não encontrado'}\n")
