"""
Catálogo de ferramentas para instalação de ar-condicionado Split.
Formato: (código, categoria, descrição, valor_aquisição, vida_útil_horas, data_atualizacao, validade_dias)
O custo/hora é calculado automaticamente: valor / vida_útil
"""

FERRAMENTAS = [
    ('FER_VACUO', 'Vácuo', 'Bomba de vácuo', 1500.00, 2000, '2025-12-30', 90),
    ('FER_MANIF', 'Manifold', 'Manifold digital', 800.00, 3000, '2025-12-30', 90),
    ('FER_SOLDA', 'Solda', 'Kit solda oxigênio/GLP', 1200.00, 1500, '2025-12-30', 90),
    ('FER_PERF', 'Furação', 'Perfuratriz/martelete', 1800.00, 2500, '2025-12-30', 90),
    ('FER_SERRA_65', 'Furação', 'Serra copo diamantada 65mm', 180.00, 150, '2025-12-30', 90),
    ('FER_SERRA_80', 'Furação', 'Serra copo diamantada 80mm', 220.00, 150, '2025-12-30', 90),
    ('FER_ESCADA', 'Acesso', 'Escada extensível 6m', 800.00, 3000, '2025-12-30', 90),
    ('FER_ANDAIME', 'Acesso', 'Andaime cavalete (par)', 600.00, 2000, '2025-12-30', 90),
    ('FER_ESTANQ', 'Teste', 'Kit teste estanqueidade', 350.00, 2000, '2025-12-30', 90),
    ('FER_MULT', 'Elétrica', 'Multímetro/alicate amperímetro', 450.00, 3000, '2025-12-30', 90),
    ('FER_MANUAL', 'Diversos', 'Ferramentas manuais (conjunto)', 1200.00, 4000, '2025-12-30', 90),
    ('FER_FURAD', 'Furação', 'Furadeira de impacto', 650.00, 2000, '2025-12-30', 90),
    ('FER_CORTA', 'Corte', 'Cortador de tubo cobre', 120.00, 1000, '2025-12-30', 90),
    ('FER_FLANG', 'Dobra', 'Flangeador/alargador', 380.00, 2000, '2025-12-30', 90),
    ('FER_BAL', 'Refrigeração', 'Balança digital refrigeração', 280.00, 2500, '2025-12-30', 90),
]
