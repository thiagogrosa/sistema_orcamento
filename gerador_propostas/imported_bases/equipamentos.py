"""
Catálogo de equipamentos de climatização.

Estrutura expandida com campos técnicos, elétricos e de tubulação.
"""
from typing import NamedTuple


class Equipamento(NamedTuple):
    """
    Equipamento de climatização.

    Grupos de campos:
    - Identificação: codigo, categoria, tipo, descricao, capacidade_btu, tecnologia, ciclo, marca, modelo
    - Elétrico: tensao_fase, alimentacao, comando
    - Tubulação: gas_pol, liquido_pol, comp_max_m
    - Técnico: pressao_pa, vazao_m3h, descarga
    - Comercial: unidade, preco, vendedor
    - Controle: atualizado_em, validade_dias
    """
    # Identificação (obrigatórios)
    codigo: str
    categoria: str  # Split, VRF, Bomba Dreno, etc.
    tipo: str  # Hi-Wall, Piso-Teto, Cassete, etc.
    descricao: str
    capacidade_btu: int  # 0 para bombas/acessórios
    tecnologia: str  # 'Inverter' ou 'On-Off'
    ciclo: str  # 'Frio' ou 'Quente/Frio'

    # Identificação (opcionais)
    marca: str = ''
    modelo: str = ''

    # Elétrico
    tensao_fase: str = '220V Mono'  # '220V Mono', '220V Tri', '380V Tri'
    alimentacao: str = ''  # Bitola do cabo: '2,5mm²', '4mm²', etc.
    comando: str = ''  # '3x1,5mm²', '5x1,0mm²', etc.

    # Tubulação
    gas_pol: str = ''  # '1/4"', '3/8"', '1/2"', '5/8"'
    liquido_pol: str = ''  # '1/4"', '3/8"', '1/2"'
    comp_max_m: int = 0  # Comprimento máximo da linha

    # Técnico (opcionais)
    pressao_pa: int = 0  # Pressão estática disponível (Pa)
    vazao_m3h: float = 0.0  # Vazão de ar (m³/h)
    descarga: str = ''  # 'V' (vertical), 'H' (horizontal), 'V/H'

    # Comercial
    unidade: str = 'UN'
    preco: float = 0.0
    vendedor: str = ''

    # Controle
    atualizado_em: str = ''
    validade_dias: int = 30


def _inferir_tubulacao(capacidade_btu: int) -> tuple[str, str]:
    """Infere bitolas de gás e líquido com base na capacidade."""
    if capacidade_btu <= 0:
        return ('', '')  # Bomba/acessório
    elif capacidade_btu <= 12000:
        return ('3/8"', '1/4"')
    elif capacidade_btu <= 22000:
        return ('5/8"', '3/8"')
    elif capacidade_btu <= 30000:
        return ('5/8"', '3/8"')
    elif capacidade_btu <= 48000:
        return ('3/4"', '3/8"')
    else:  # >= 60000
        return ('7/8"', '1/2"')


def _inferir_alimentacao(capacidade_btu: int, tensao: str) -> str:
    """Infere bitola do cabo de alimentação com base na capacidade e tensão."""
    if capacidade_btu <= 0:
        return ''  # Bomba/acessório
    elif capacidade_btu <= 12000:
        return '2,5mm²'
    elif capacidade_btu <= 24000:
        return '4mm²'
    elif capacidade_btu <= 36000:
        return '6mm²' if 'Mono' in tensao else '4mm²'
    else:
        return '10mm²' if 'Mono' in tensao else '6mm²'


# Dados migrados com novos campos
EQUIPAMENTOS = [
    # Splits Hi-Wall Inverter
    Equipamento(
        codigo='EQP_HW_9K',
        categoria='Split',
        tipo='Hi-Wall',
        descricao='Split Hi-Wall Inverter 9.000 BTUs',
        capacidade_btu=9000,
        tecnologia='Inverter',
        ciclo='Frio',
        tensao_fase='220V Mono',
        alimentacao='2,5mm²',
        comando='5x1,0mm²',
        gas_pol='3/8"',
        liquido_pol='1/4"',
        comp_max_m=15,
        unidade='UN',
        preco=1800.00,
        atualizado_em='2025-12-30',
        validade_dias=30
    ),
    Equipamento(
        codigo='EQP_HW_12K',
        categoria='Split',
        tipo='Hi-Wall',
        descricao='Split Hi-Wall Inverter 12.000 BTUs',
        capacidade_btu=12000,
        tecnologia='Inverter',
        ciclo='Frio',
        tensao_fase='220V Mono',
        alimentacao='2,5mm²',
        comando='5x1,0mm²',
        gas_pol='3/8"',
        liquido_pol='1/4"',
        comp_max_m=20,
        unidade='UN',
        preco=2200.00,
        atualizado_em='2025-12-30',
        validade_dias=30
    ),
    Equipamento(
        codigo='EQP_HW_18K',
        categoria='Split',
        tipo='Hi-Wall',
        descricao='Split Hi-Wall Inverter 18.000 BTUs',
        capacidade_btu=18000,
        tecnologia='Inverter',
        ciclo='Frio',
        tensao_fase='220V Mono',
        alimentacao='4mm²',
        comando='5x1,0mm²',
        gas_pol='5/8"',
        liquido_pol='3/8"',
        comp_max_m=25,
        unidade='UN',
        preco=3200.00,
        atualizado_em='2025-12-30',
        validade_dias=30
    ),
    Equipamento(
        codigo='EQP_HW_22K',
        categoria='Split',
        tipo='Hi-Wall',
        descricao='Split Hi-Wall Inverter 22.000 BTUs',
        capacidade_btu=22000,
        tecnologia='Inverter',
        ciclo='Frio',
        tensao_fase='220V Mono',
        alimentacao='4mm²',
        comando='5x1,0mm²',
        gas_pol='5/8"',
        liquido_pol='3/8"',
        comp_max_m=25,
        unidade='UN',
        preco=3800.00,
        atualizado_em='2025-12-30',
        validade_dias=30
    ),
    Equipamento(
        codigo='EQP_HW_24K',
        categoria='Split',
        tipo='Hi-Wall',
        descricao='Split Hi-Wall Inverter 24.000 BTUs',
        capacidade_btu=24000,
        tecnologia='Inverter',
        ciclo='Frio',
        tensao_fase='220V Mono',
        alimentacao='4mm²',
        comando='5x1,0mm²',
        gas_pol='5/8"',
        liquido_pol='3/8"',
        comp_max_m=25,
        unidade='UN',
        preco=4200.00,
        atualizado_em='2025-12-30',
        validade_dias=30
    ),
    Equipamento(
        codigo='EQP_HW_30K',
        categoria='Split',
        tipo='Hi-Wall',
        descricao='Split Hi-Wall Inverter 30.000 BTUs',
        capacidade_btu=30000,
        tecnologia='Inverter',
        ciclo='Frio',
        tensao_fase='220V Mono',
        alimentacao='6mm²',
        comando='5x1,0mm²',
        gas_pol='5/8"',
        liquido_pol='3/8"',
        comp_max_m=30,
        unidade='UN',
        preco=5500.00,
        atualizado_em='2025-12-30',
        validade_dias=30
    ),

    # Splits Piso-Teto
    Equipamento(
        codigo='EQP_PT_36K',
        categoria='Split',
        tipo='Piso-Teto',
        descricao='Split Piso-Teto 36.000 BTUs',
        capacidade_btu=36000,
        tecnologia='On-Off',
        ciclo='Frio',
        tensao_fase='220V Mono',
        alimentacao='6mm²',
        comando='5x1,0mm²',
        gas_pol='3/4"',
        liquido_pol='3/8"',
        comp_max_m=30,
        unidade='UN',
        preco=7200.00,
        atualizado_em='2025-12-30',
        validade_dias=30
    ),
    Equipamento(
        codigo='EQP_PT_48K',
        categoria='Split',
        tipo='Piso-Teto',
        descricao='Split Piso-Teto 48.000 BTUs',
        capacidade_btu=48000,
        tecnologia='On-Off',
        ciclo='Frio',
        tensao_fase='220V Tri',
        alimentacao='6mm²',
        comando='5x1,0mm²',
        gas_pol='3/4"',
        liquido_pol='3/8"',
        comp_max_m=40,
        unidade='UN',
        preco=9500.00,
        atualizado_em='2025-12-30',
        validade_dias=30
    ),
    Equipamento(
        codigo='EQP_PT_60K',
        categoria='Split',
        tipo='Piso-Teto',
        descricao='Split Piso-Teto 60.000 BTUs',
        capacidade_btu=60000,
        tecnologia='On-Off',
        ciclo='Frio',
        tensao_fase='220V Tri',
        alimentacao='10mm²',
        comando='5x1,0mm²',
        gas_pol='7/8"',
        liquido_pol='1/2"',
        comp_max_m=50,
        unidade='UN',
        preco=12000.00,
        atualizado_em='2025-12-30',
        validade_dias=30
    ),

    # Bombas de Dreno
    Equipamento(
        codigo='EQP_BOMB_P',
        categoria='Bomba Dreno',
        tipo='Mini',
        descricao='Bomba dreno mini (até 12.000 BTUs)',
        capacidade_btu=0,
        tecnologia='-',
        ciclo='-',
        unidade='UN',
        preco=320.00,
        atualizado_em='2025-12-30',
        validade_dias=30
    ),
    Equipamento(
        codigo='EQP_BOMB_M',
        categoria='Bomba Dreno',
        tipo='Média',
        descricao='Bomba dreno média (até 36.000 BTUs)',
        capacidade_btu=0,
        tecnologia='-',
        ciclo='-',
        unidade='UN',
        preco=480.00,
        atualizado_em='2025-12-30',
        validade_dias=30
    ),
    Equipamento(
        codigo='EQP_BOMB_G',
        categoria='Bomba Dreno',
        tipo='Grande',
        descricao='Bomba dreno grande (até 60.000 BTUs)',
        capacidade_btu=0,
        tecnologia='-',
        ciclo='-',
        unidade='UN',
        preco=650.00,
        atualizado_em='2025-12-30',
        validade_dias=30
    ),
]
