"""
Catálogo de mão de obra para instalação de ar-condicionado Split.
Formato: (código, categoria, descrição, unidade, custo, data_atualizacao, validade_dias)
"""

MAO_DE_OBRA = [
    ('MO_TEC', 'Instalação', 'Técnico em refrigeração', 'H', 65.00, '2025-12-30', 30),
    ('MO_AJU', 'Instalação', 'Ajudante de instalação', 'H', 35.00, '2025-12-30', 30),
    ('MO_ELE', 'Elétrica', 'Eletricista', 'H', 55.00, '2025-12-30', 30),
    ('MO_PED', 'Civil', 'Pedreiro', 'H', 50.00, '2025-12-30', 30),
    ('MO_SERV', 'Civil', 'Servente de pedreiro', 'H', 30.00, '2025-12-30', 30),
    ('MO_ALT', 'Adicional', 'Adicional trabalho em altura (>3m)', 'H', 25.00, '2025-12-30', 30),
    ('MO_FAC', 'Adicional', 'Adicional trabalho fachada', 'H', 35.00, '2025-12-30', 30),
    ('MO_DESL_20', 'Deslocamento', 'Deslocamento equipe (até 20km)', 'VZ', 80.00, '2025-12-30', 30),
    ('MO_DESL_50', 'Deslocamento', 'Deslocamento equipe (20-50km)', 'VZ', 150.00, '2025-12-30', 30),
]
