"""
Sistema de metricas para rastreamento de consumo
"""

import json
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional
from dataclasses import dataclass, field, asdict


@dataclass
class Metricas:
    """Armazena metricas de um orcamento"""

    # Identificacao
    orcamento_id: str = ""
    inicio: str = ""
    fim: str = ""

    # Tempos (segundos)
    tempo_compositor: float = 0.0
    tempo_precificador: float = 0.0
    tempo_pdf: float = 0.0
    tempo_total: float = 0.0

    # Tamanhos de arquivo (bytes)
    tamanho_escopo: int = 0
    tamanho_composicao: int = 0
    tamanho_precificado: int = 0
    tamanho_pdf: int = 0

    # Estimativa de tokens (baseado em chars / 3.5 para portugues)
    tokens_escopo: int = 0
    tokens_composicao: int = 0
    tokens_precificado: int = 0
    tokens_total_dados: int = 0

    # Contadores
    qtd_itens: int = 0
    qtd_materiais: int = 0
    qtd_mao_obra: int = 0
    qtd_ferramentas: int = 0

    # Valores
    valor_total: float = 0.0

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    def salvar(self, path: Path):
        """Salva metricas em arquivo JSON"""
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(self.to_dict(), f, ensure_ascii=False, indent=2)

    @classmethod
    def carregar(cls, path: Path) -> 'Metricas':
        """Carrega metricas de arquivo JSON"""
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return cls(**data)


class RastreadorMetricas:
    """Rastreia metricas durante processamento"""

    def __init__(self, orcamento_id: str = ""):
        self.metricas = Metricas(
            orcamento_id=orcamento_id,
            inicio=datetime.now().isoformat()
        )
        self._inicio_etapa: Optional[float] = None
        self._inicio_total: float = time.time()

    def iniciar_etapa(self):
        """Marca inicio de uma etapa"""
        self._inicio_etapa = time.time()

    def finalizar_etapa(self, nome_etapa: str):
        """Finaliza etapa e registra tempo"""
        if self._inicio_etapa is None:
            return

        duracao = time.time() - self._inicio_etapa

        if nome_etapa == "compositor":
            self.metricas.tempo_compositor = round(duracao, 3)
        elif nome_etapa == "precificador":
            self.metricas.tempo_precificador = round(duracao, 3)
        elif nome_etapa == "pdf":
            self.metricas.tempo_pdf = round(duracao, 3)

        self._inicio_etapa = None

    def registrar_arquivo(self, nome: str, path: Path):
        """Registra metricas de um arquivo"""
        if not path.exists():
            return

        tamanho = path.stat().st_size

        # Ler conteudo para contar caracteres
        try:
            with open(path, 'r', encoding='utf-8') as f:
                conteudo = f.read()
            chars = len(conteudo)
            tokens_estimados = int(chars / 3.5)  # ~3.5 chars por token em PT
        except:
            tokens_estimados = int(tamanho / 4)

        if nome == "escopo":
            self.metricas.tamanho_escopo = tamanho
            self.metricas.tokens_escopo = tokens_estimados
        elif nome == "composicao":
            self.metricas.tamanho_composicao = tamanho
            self.metricas.tokens_composicao = tokens_estimados
        elif nome == "precificado":
            self.metricas.tamanho_precificado = tamanho
            self.metricas.tokens_precificado = tokens_estimados
        elif nome == "pdf":
            self.metricas.tamanho_pdf = tamanho

    def registrar_resultado(self, precificado: Dict[str, Any]):
        """Registra metricas do resultado"""
        self.metricas.qtd_itens = len(precificado.get('itens_precificados', []))

        resumo = precificado.get('resumo_financeiro', {})
        self.metricas.valor_total = resumo.get('valor_total', 0)

        # Contar insumos
        for item in precificado.get('itens_precificados', []):
            self.metricas.qtd_materiais += len(item.get('materiais', []))
            self.metricas.qtd_mao_obra += len(item.get('mao_de_obra', []))
            self.metricas.qtd_ferramentas += len(item.get('ferramentas', []))

    def finalizar(self) -> Metricas:
        """Finaliza rastreamento e retorna metricas"""
        self.metricas.fim = datetime.now().isoformat()
        self.metricas.tempo_total = round(time.time() - self._inicio_total, 3)
        self.metricas.tokens_total_dados = (
            self.metricas.tokens_escopo +
            self.metricas.tokens_composicao +
            self.metricas.tokens_precificado
        )
        return self.metricas


def formatar_metricas(metricas: Metricas) -> str:
    """Formata metricas para exibicao"""
    return f"""
## Metricas do Orcamento

### Tempos de Processamento
| Etapa | Tempo |
|-------|------:|
| Compositor | {metricas.tempo_compositor:.3f}s |
| Precificador | {metricas.tempo_precificador:.3f}s |
| PDF | {metricas.tempo_pdf:.3f}s |
| **Total** | **{metricas.tempo_total:.3f}s** |

### Tamanho dos Dados
| Arquivo | Tamanho | Tokens (est.) |
|---------|--------:|--------------:|
| escopo.json | {metricas.tamanho_escopo:,} bytes | {metricas.tokens_escopo:,} |
| composicao.json | {metricas.tamanho_composicao:,} bytes | {metricas.tokens_composicao:,} |
| precificado.json | {metricas.tamanho_precificado:,} bytes | {metricas.tokens_precificado:,} |
| **Total dados** | | **{metricas.tokens_total_dados:,}** |

### Contadores
- Itens: {metricas.qtd_itens}
- Materiais: {metricas.qtd_materiais}
- Mao de obra: {metricas.qtd_mao_obra}
- Ferramentas: {metricas.qtd_ferramentas}

### Resultado
- **Valor Total:** R$ {metricas.valor_total:,.2f}
"""
