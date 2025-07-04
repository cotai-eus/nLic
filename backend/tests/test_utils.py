import pytest
from app.utils.filters import filtrar_por_palavra_chave

def test_filtrar_por_palavra_chave():
    # Teste com palavra-chave presente
    assert filtrar_por_palavra_chave("Objeto de compra de TI", ["TI"])
    assert filtrar_por_palavra_chave("Serviços de Limpeza", ["limpeza"])
    assert filtrar_por_palavra_chave("Material de Escritório", ["material", "escritório"])

    # Teste com palavra-chave ausente
    assert not filtrar_por_palavra_chave("Objeto de compra de TI", ["construção"])
    assert not filtrar_por_palavra_chave("Serviços de Limpeza", ["segurança"])

    # Teste com lista de palavras-chave vazia
    assert not filtrar_por_palavra_chave("Qualquer objeto", [])

    # Teste case-insensitive
    assert filtrar_por_palavra_chave("Objeto de Compra de TI", ["ti"])
    assert filtrar_por_palavra_chave("Serviços de limpeza", ["LIMPEZA"])
