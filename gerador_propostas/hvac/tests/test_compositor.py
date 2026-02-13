"""
Testes do modulo compositor
"""

import pytest
from hvac.compositor import (
    gerar_descricao,
    calcular_quantidade,
    consolidar_itens,
    processar
)


class TestGerarDescricao:
    """Testes para geracao de descricao"""

    def test_descricao_simples_sem_variavel(self):
        """Composicao sem descricao_variavel usa descricao simples"""
        comp = {"descricao": "Adicional suporte"}
        assert gerar_descricao(comp, 0) == "Adicional suporte"

    def test_descricao_variavel_singular(self):
        """Usa unidade singular quando variavel = 1"""
        comp = {
            "descricao": "Instalacao",
            "descricao_variavel": {
                "prefixo": "Instalacao com ",
                "sufixo": " de linha",
                "unidade_singular": "metro",
                "unidade_plural": "metros"
            }
        }
        assert gerar_descricao(comp, 1) == "Instalacao com 1 metro de linha"

    def test_descricao_variavel_plural(self):
        """Usa unidade plural quando variavel > 1"""
        comp = {
            "descricao": "Instalacao",
            "descricao_variavel": {
                "prefixo": "Instalacao com ",
                "sufixo": " de linha",
                "unidade_singular": "metro",
                "unidade_plural": "metros"
            }
        }
        assert gerar_descricao(comp, 5) == "Instalacao com 5 metros de linha"

    def test_descricao_variavel_decimal(self):
        """Formata valores decimais corretamente"""
        comp = {
            "descricao_variavel": {
                "prefixo": "Dreno com ",
                "sufixo": "",
                "unidade_singular": "metro",
                "unidade_plural": "metros"
            }
        }
        assert gerar_descricao(comp, 3.5) == "Dreno com 3.5 metros"


class TestCalcularQuantidade:
    """Testes para calculo de quantidade"""

    def test_apenas_qtd_base(self):
        """Item com apenas qtd_base"""
        item = {"qtd_base": 5, "qtd_var": 0}
        assert calcular_quantidade(item, 10) == 5

    def test_apenas_qtd_var(self):
        """Item com apenas qtd_var"""
        item = {"qtd_base": 0, "qtd_var": 1.1}
        assert calcular_quantidade(item, 10) == 11.0

    def test_qtd_base_e_var(self):
        """Item com qtd_base e qtd_var"""
        item = {"qtd_base": 2, "qtd_var": 0.5}
        assert calcular_quantidade(item, 8) == 6.0  # 2 + (0.5 * 8)

    def test_variavel_zero(self):
        """Variavel zero retorna apenas qtd_base"""
        item = {"qtd_base": 3, "qtd_var": 1.5}
        assert calcular_quantidade(item, 0) == 3


class TestConsolidarItens:
    """Testes para consolidacao de itens"""

    def test_itens_diferentes(self):
        """Itens diferentes nao sao consolidados"""
        itens = [
            {"codigo": "A", "descricao": "Item A", "quantidade": 5, "unidade": "UN"},
            {"codigo": "B", "descricao": "Item B", "quantidade": 3, "unidade": "M"}
        ]
        resultado = consolidar_itens(itens)
        assert len(resultado) == 2

    def test_itens_iguais(self):
        """Itens iguais tem quantidades somadas"""
        itens = [
            {"codigo": "A", "descricao": "Item A", "quantidade": 5, "unidade": "UN"},
            {"codigo": "A", "descricao": "Item A", "quantidade": 3, "unidade": "UN"}
        ]
        resultado = consolidar_itens(itens)
        assert len(resultado) == 1
        assert resultado[0]["quantidade"] == 8

    def test_ordenacao_por_codigo(self):
        """Resultado e ordenado por codigo"""
        itens = [
            {"codigo": "C", "descricao": "Item C", "quantidade": 1, "unidade": "UN"},
            {"codigo": "A", "descricao": "Item A", "quantidade": 1, "unidade": "UN"},
            {"codigo": "B", "descricao": "Item B", "quantidade": 1, "unidade": "UN"}
        ]
        resultado = consolidar_itens(itens)
        codigos = [item["codigo"] for item in resultado]
        assert codigos == ["A", "B", "C"]


class TestProcessar:
    """Testes para processamento completo"""

    def test_escopo_vazio(self):
        """Escopo sem itens gera composicao vazia"""
        escopo = {"projeto": {"nome": "Teste"}, "itens": []}
        bases = {
            "composicoes": {},
            "materiais": {},
            "mao_de_obra": {},
            "ferramentas": {},
            "equipamentos": {},
            "bdi": {}
        }
        resultado = processar(escopo, bases)
        assert resultado["projeto"] == "Teste"
        assert resultado["itens_orcamento"] == []

    def test_composicao_nao_encontrada(self):
        """Composicao inexistente gera observacao"""
        escopo = {
            "projeto": {"nome": "Teste"},
            "itens": [{"composicao": "INEXISTENTE", "variavel": 5, "quantidade": 1}]
        }
        bases = {
            "composicoes": {},
            "materiais": {},
            "mao_de_obra": {},
            "ferramentas": {},
            "equipamentos": {},
            "bdi": {}
        }
        resultado = processar(escopo, bases)
        assert any("nao encontrada" in obs for obs in resultado["observacoes"])
