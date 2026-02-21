"""
Testes do modulo precificador
"""

import pytest
from datetime import date, timedelta
from hvac.precificador import (
    obter_preco_item,
    verificar_preco_desatualizado,
    precificar_lista,
    processar
)


class TestObterPrecoItem:
    """Testes para obtencao de preco"""

    def test_material_com_preco(self):
        """Material retorna preco"""
        bases = {"materiais": {"MAT_001": {"preco": 25.50, "data_atualizacao": "2025-01-01"}}}
        preco, data = obter_preco_item(bases, "MAT", "MAT_001")
        assert preco == 25.50
        assert data == "2025-01-01"

    def test_mao_obra_custo_hora(self):
        """Mao de obra retorna custo_hora"""
        bases = {"mao_de_obra": {"MO_TEC": {"custo_hora": 65.00}}}
        preco, _ = obter_preco_item(bases, "MO", "MO_TEC")
        assert preco == 65.00

    def test_ferramenta_custo_hora(self):
        """Ferramenta retorna custo_hora"""
        bases = {"ferramentas": {"FER_001": {"custo_hora": 0.75}}}
        preco, _ = obter_preco_item(bases, "FER", "FER_001")
        assert preco == 0.75

    def test_item_inexistente(self):
        """Item inexistente retorna zero"""
        bases = {"materiais": {}}
        preco, data = obter_preco_item(bases, "MAT", "NAO_EXISTE")
        assert preco == 0.0
        assert data is None


class TestVerificarPrecoDesatualizado:
    """Testes para verificacao de desatualizacao"""

    def test_preco_atual(self):
        """Preco recente retorna None"""
        data_recente = date.today().isoformat()
        assert verificar_preco_desatualizado(data_recente) is None

    def test_preco_alerta(self):
        """Preco com mais de 90 dias retorna alerta"""
        data_antiga = (date.today() - timedelta(days=100)).isoformat()
        assert verificar_preco_desatualizado(data_antiga) == "alerta"

    def test_preco_critico(self):
        """Preco com mais de 180 dias retorna critico"""
        data_muito_antiga = (date.today() - timedelta(days=200)).isoformat()
        assert verificar_preco_desatualizado(data_muito_antiga) == "critico"

    def test_sem_data(self):
        """Sem data retorna critico"""
        assert verificar_preco_desatualizado(None) == "critico"


class TestPrecificarLista:
    """Testes para precificacao de lista"""

    def test_lista_vazia(self):
        """Lista vazia retorna lista vazia e custo zero"""
        bases = {"materiais": {}}
        resultado, custo = precificar_lista([], "MAT", bases, [])
        assert resultado == []
        assert custo == 0.0

    def test_precificacao_simples(self):
        """Precifica item corretamente"""
        bases = {
            "materiais": {
                "TUB_14": {
                    "descricao": "Tubo 1/4",
                    "preco": 18.00,
                    "data_atualizacao": date.today().isoformat()
                }
            }
        }
        itens = [{"codigo": "TUB_14", "descricao": "Tubo 1/4", "quantidade": 10, "unidade": "M"}]
        alertas = []

        resultado, custo = precificar_lista(itens, "MAT", bases, alertas)

        assert len(resultado) == 1
        assert resultado[0]["preco_unitario"] == 18.00
        assert resultado[0]["custo"] == 180.00
        assert custo == 180.00
        assert len(alertas) == 0


class TestProcessar:
    """Testes para processamento completo"""

    def test_composicao_vazia(self):
        """Composicao sem itens gera orcamento vazio"""
        composicao = {
            "projeto": "Teste",
            "cliente": "Cliente Teste",
            "itens_orcamento": []
        }
        bases = {
            "materiais": {},
            "mao_de_obra": {},
            "ferramentas": {},
            "equipamentos": {},
            "bdi": {
                "MAT": {"percentual": 0.35},
                "MO": {"percentual": 0.40},
                "FER": {"percentual": 0.30},
                "EQP": {"percentual": 0.25}
            }
        }

        resultado = processar(composicao, bases)

        assert resultado["projeto"] == "Teste"
        assert resultado["resumo_financeiro"]["valor_total"] == 0.0

    def test_calculo_bdi(self):
        """BDI e calculado corretamente por categoria"""
        composicao = {
            "projeto": "Teste BDI",
            "itens_orcamento": [{
                "id": 1,
                "descricao": "Item teste",
                "materiais": [{"codigo": "MAT1", "descricao": "Material", "quantidade": 1, "unidade": "UN"}],
                "mao_de_obra": [],
                "ferramentas": [],
                "equipamentos": []
            }]
        }
        bases = {
            "materiais": {"MAT1": {"preco": 100.00, "data_atualizacao": date.today().isoformat()}},
            "mao_de_obra": {},
            "ferramentas": {},
            "equipamentos": {},
            "bdi": {
                "MAT": {"percentual": 0.35},
                "MO": {"percentual": 0.40},
                "FER": {"percentual": 0.30},
                "EQP": {"percentual": 0.25}
            }
        }

        resultado = processar(composicao, bases)

        resumo = resultado["resumo_financeiro"]
        assert resumo["total_materiais"] == 100.00
        assert resumo["bdi_materiais"] == 35.00  # 100 * 0.35
        assert resumo["valor_total"] == 135.00  # 100 + 35
