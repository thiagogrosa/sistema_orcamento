"""
Catálogo de equipamentos de climatização.
Formato: (código, categoria, descrição, capacidade_btu, unidade, preço, data_atualizacao, validade_dias)
"""

EQUIPAMENTOS = [
    # Hi-Wall (uso residencial e comercial leve)
    ('EQP_HW_9K', 'Split Hi-Wall', 'Split Hi-Wall Inverter 9.000 BTUs', 9000, 'UN', 1800.00, '2026-01-21', 30),
    ('EQP_HW_12K', 'Split Hi-Wall', 'Split Hi-Wall Inverter 12.000 BTUs', 12000, 'UN', 2200.00, '2026-01-21', 30),
    ('EQP_HW_18K', 'Split Hi-Wall', 'Split Hi-Wall Inverter 18.000 BTUs', 18000, 'UN', 3200.00, '2026-01-21', 30),
    ('EQP_HW_22K', 'Split Hi-Wall', 'Split Hi-Wall Inverter 22.000 BTUs', 22000, 'UN', 3800.00, '2026-01-21', 30),
    ('EQP_HW_24K', 'Split Hi-Wall', 'Split Hi-Wall Inverter 24.000 BTUs', 24000, 'UN', 4200.00, '2026-01-21', 30),
    ('EQP_HW_30K', 'Split Hi-Wall', 'Split Hi-Wall Inverter 30.000 BTUs', 30000, 'UN', 5500.00, '2026-01-21', 30),

    # Cassete 4 Vias (comercial, embutido no forro)
    ('EQP_CS4_18K', 'Split Cassete 4 Vias', 'Split Cassete 4 Vias Inverter 18.000 BTUs', 18000, 'UN', 4500.00, '2026-01-21', 30),
    ('EQP_CS4_24K', 'Split Cassete 4 Vias', 'Split Cassete 4 Vias Inverter 24.000 BTUs', 24000, 'UN', 5800.00, '2026-01-21', 30),
    ('EQP_CS4_36K', 'Split Cassete 4 Vias', 'Split Cassete 4 Vias Inverter 36.000 BTUs', 36000, 'UN', 8200.00, '2026-01-21', 30),
    ('EQP_CS4_48K', 'Split Cassete 4 Vias', 'Split Cassete 4 Vias Inverter 48.000 BTUs', 48000, 'UN', 10500.00, '2026-01-21', 30),
    ('EQP_CS4_60K', 'Split Cassete 4 Vias', 'Split Cassete 4 Vias Inverter 60.000 BTUs', 60000, 'UN', 13500.00, '2026-01-21', 30),

    # Piso-Teto (comercial, versátil)
    ('EQP_PT_18K', 'Split Piso-Teto', 'Split Piso-Teto Inverter 18.000 BTUs', 18000, 'UN', 4200.00, '2026-01-21', 30),
    ('EQP_PT_24K', 'Split Piso-Teto', 'Split Piso-Teto Inverter 24.000 BTUs', 24000, 'UN', 5500.00, '2026-01-21', 30),
    ('EQP_PT_36K', 'Split Piso-Teto', 'Split Piso-Teto Inverter 36.000 BTUs', 36000, 'UN', 7200.00, '2026-01-21', 30),
    ('EQP_PT_48K', 'Split Piso-Teto', 'Split Piso-Teto Inverter 48.000 BTUs', 48000, 'UN', 9500.00, '2026-01-21', 30),
    ('EQP_PT_60K', 'Split Piso-Teto', 'Split Piso-Teto Inverter 60.000 BTUs', 60000, 'UN', 12000.00, '2026-01-21', 30),

    # Cassete 1 Via (comercial, direcional)
    ('EQP_CS1_18K', 'Split Cassete 1 Via', 'Split Cassete 1 Via Inverter 18.000 BTUs', 18000, 'UN', 4000.00, '2026-01-21', 30),
    ('EQP_CS1_24K', 'Split Cassete 1 Via', 'Split Cassete 1 Via Inverter 24.000 BTUs', 24000, 'UN', 5200.00, '2026-01-21', 30),
    ('EQP_CS1_36K', 'Split Cassete 1 Via', 'Split Cassete 1 Via Inverter 36.000 BTUs', 36000, 'UN', 7500.00, '2026-01-21', 30),

    # Built-in / Dutado (comercial, flexível com dutos)
    ('EQP_BI_18K', 'Split Built-in', 'Split Built-in (Dutado) Inverter 18.000 BTUs', 18000, 'UN', 3800.00, '2026-01-21', 30),
    ('EQP_BI_24K', 'Split Built-in', 'Split Built-in (Dutado) Inverter 24.000 BTUs', 24000, 'UN', 4900.00, '2026-01-21', 30),
    ('EQP_BI_36K', 'Split Built-in', 'Split Built-in (Dutado) Inverter 36.000 BTUs', 36000, 'UN', 7000.00, '2026-01-21', 30),

    # Acessórios - Bombas de Dreno
    ('EQP_BOMB_P', 'Bomba Dreno', 'Bomba dreno mini (até 12.000 BTUs)', 0, 'UN', 320.00, '2026-01-21', 30),
    ('EQP_BOMB_M', 'Bomba Dreno', 'Bomba dreno média (até 36.000 BTUs)', 0, 'UN', 480.00, '2026-01-21', 30),
    ('EQP_BOMB_G', 'Bomba Dreno', 'Bomba dreno grande (até 60.000 BTUs)', 0, 'UN', 650.00, '2026-01-21', 30),
]
