"""
Carregador de bases de dados JSON
"""

import json
from pathlib import Path
from typing import Dict, Any, Optional


def get_bases_dir() -> Path:
    """Retorna o diretorio das bases de dados"""
    # Assume que as bases estao em bases/ relativo a raiz do projeto
    current = Path(__file__).resolve()
    # hvac/utils/loader.py -> hvac/utils -> hvac -> projeto
    projeto_dir = current.parent.parent.parent
    return projeto_dir / "bases"


def carregar_json(nome_arquivo: str, bases_dir: Optional[Path] = None) -> Dict[str, Any]:
    """
    Carrega um arquivo JSON das bases

    Args:
        nome_arquivo: Nome do arquivo (ex: 'materiais.json')
        bases_dir: Diretorio das bases (opcional, usa padrao se nao informado)

    Returns:
        Dicionario com o conteudo do JSON
    """
    if bases_dir is None:
        bases_dir = get_bases_dir()

    caminho = bases_dir / nome_arquivo

    if not caminho.exists():
        raise FileNotFoundError(f"Base nao encontrada: {caminho}")

    with open(caminho, "r", encoding="utf-8") as f:
        return json.load(f)


def carregar_bases(bases_dir: Optional[Path] = None) -> Dict[str, Dict[str, Any]]:
    """
    Carrega todas as bases de dados necessarias

    Returns:
        Dicionario com todas as bases carregadas:
        {
            'materiais': {...},
            'mao_de_obra': {...},
            'ferramentas': {...},
            'equipamentos': {...},
            'composicoes': {...},
            'bdi': {...}
        }
    """
    arquivos = [
        "materiais.json",
        "mao_de_obra.json",
        "ferramentas.json",
        "equipamentos.json",
        "composicoes.json",
        "bdi.json"
    ]

    bases = {}
    for arquivo in arquivos:
        nome = arquivo.replace(".json", "")
        try:
            dados = carregar_json(arquivo, bases_dir)
            # Remove o wrapper (ex: {"materiais": {...}} -> {...})
            if nome in dados:
                bases[nome] = dados[nome]
            elif nome == "mao_de_obra" and "mao_obra" in dados:
                bases[nome] = dados["mao_obra"]
            else:
                bases[nome] = dados
        except FileNotFoundError:
            print(f"Aviso: Base {arquivo} nao encontrada")
            bases[nome] = {}

    return bases


def obter_item(bases: Dict, tipo: str, codigo: str) -> Optional[Dict[str, Any]]:
    """
    Obtem um item de uma base pelo codigo

    Args:
        bases: Dicionario com todas as bases
        tipo: Tipo do item (MAT, MO, FER, EQP)
        codigo: Codigo do item

    Returns:
        Dicionario com os dados do item ou None se nao encontrado
    """
    mapa_tipo = {
        "MAT": "materiais",
        "MO": "mao_de_obra",
        "FER": "ferramentas",
        "EQP": "equipamentos"
    }

    nome_base = mapa_tipo.get(tipo)
    if not nome_base:
        return None

    base = bases.get(nome_base, {})
    return base.get(codigo)


def obter_composicao(bases: Dict, codigo: str) -> Optional[Dict[str, Any]]:
    """
    Obtem uma composicao pelo codigo

    Args:
        bases: Dicionario com todas as bases
        codigo: Codigo da composicao (ex: COMP_INST_9K)

    Returns:
        Dicionario com os dados da composicao ou None se nao encontrada
    """
    composicoes = bases.get("composicoes", {})
    return composicoes.get(codigo)


def obter_bdi(bases: Dict, tipo: str) -> float:
    """
    Obtem o percentual de BDI para um tipo de insumo

    Args:
        bases: Dicionario com todas as bases
        tipo: Tipo do insumo (MAT, MO, FER, EQP)

    Returns:
        Percentual de BDI (ex: 0.35 para 35%)
    """
    bdi = bases.get("bdi", {})
    item_bdi = bdi.get(tipo, {})
    return item_bdi.get("percentual", 0.0)
