def filtrar_por_palavra_chave(objeto_compra: str, palavras_chave: list[str]) -> bool:
    objeto = objeto_compra.lower()
    return any(palavra.lower() in objeto for palavra in palavras_chave)
