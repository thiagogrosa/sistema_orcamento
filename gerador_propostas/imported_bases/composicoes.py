"""
Composições de serviço para instalação de ar-condicionado Split.
Cada composição agrupa materiais, mão de obra e ferramentas.

Formato:
- codigo: Identificador único
- descricao: Descrição curta
- desc_pre: Texto antes da variável (opcional)
- desc_pos: Texto após a variável (opcional)
- unid_sing: Unidade variável singular (opcional, ex: "metro")
- unid_plur: Unidade variável plural (opcional, ex: "metros")
- itens: Lista de (Tipo, Código, Qtd_Base, Qtd_por_Metro)
"""

COMPOSICOES = [
    {
        'codigo': 'COMP_INST_9K',
        'descricao': 'Instalação Split 9.000 BTUs',
        'desc_pre': 'Instalação Split 9.000 BTUs com ',
        'desc_pos': ' de linha frigorígena',
        'unid_sing': 'metro',
        'unid_plur': 'metros',
        'itens': [
            ('MAT', 'TUB_14_FLEX', 0, 1.1),
            ('MAT', 'TUB_38_FLEX', 0, 1.1),
            ('MAT', 'ISO_14_ELA_E9', 0, 1.1),
            ('MAT', 'ISO_38_ELA_E9', 0, 1.1),
            ('MAT', 'ACA_FITA_TER', 0.15, 0),
            ('MAT', 'CAB_COM', 0, 1.15),
            ('MAT', 'SUP_EVAP', 1, 0),
            ('MAT', 'SUP_BUCHA', 6, 0),
            ('MAT', 'SUP_CHIP', 6, 0),
            ('MAT', 'ACA_ESPUMA', 0.3, 0),
            ('MAT', 'ACA_FITA_ISO', 0.25, 0),
            ('MAT', 'ACA_FITA_AUT', 0.2, 0),
            ('MAT', 'SOL_PRATA', 2, 0),
            ('MAT', 'SOL_FLUXO', 0.2, 0),
            ('MO', 'MO_TEC', 2, 0.15),
            ('MO', 'MO_AJU', 2, 0.15),
            ('FER', 'FER_VACUO', 0.5, 0),
            ('FER', 'FER_MANIF', 0.5, 0),
            ('FER', 'FER_SOLDA', 0.5, 0),
            ('FER', 'FER_MANUAL', 2.5, 0),
        ]
    },
    {
        'codigo': 'COMP_SUP_MF',
        'descricao': 'Adicional suporte mão francesa 400mm (condensadora)',
        'itens': [
            ('MAT', 'SUP_MF_400', 1, 0),
            ('MAT', 'SUP_PARF_100', 4, 0),
            ('MO', 'MO_TEC', 0.75, 0),
            ('MO', 'MO_AJU', 0.75, 0),
            ('FER', 'FER_PERF', 0.5, 0),
        ]
    },
    {
        'codigo': 'COMP_SUP_CALCO',
        'descricao': 'Adicional calços de borracha (condensadora)',
        'itens': [
            ('MAT', 'SUP_CALCO', 1, 0),
            ('MO', 'MO_TEC', 0.25, 0),
        ]
    },
    {
        'codigo': 'COMP_ELE',
        'descricao': 'Alimentação elétrica 220V mono',
        'desc_pre': 'Alimentação elétrica 220V mono com ',
        'desc_pos': ' de cabo e eletroduto',
        'unid_sing': 'metro',
        'unid_plur': 'metros',
        'itens': [
            ('MAT', 'CAB_PP_25', 0, 1.1),
            ('MAT', 'COND_CORR_34', 0, 1.1),
            ('MAT', 'COND_CURV_34', 2, 0),
            ('MAT', 'COND_ABRC_34', 0, 1.2),
            ('MAT', 'ACA_FITA_ISO', 0.25, 0),
            ('MO', 'MO_ELE', 1, 0.15),
            ('FER', 'FER_MULT', 0.5, 0),
        ]
    },
    {
        'codigo': 'COMP_DRN_CRIS',
        'descricao': 'Dreno mangueira cristal',
        'desc_pre': 'Dreno mangueira cristal com ',
        'desc_pos': '',
        'unid_sing': 'metro',
        'unid_plur': 'metros',
        'itens': [
            ('MAT', 'DRN_CRIS_34', 0, 1.1),
            ('MAT', 'DRN_ABRC', 0, 1.3),
            ('MO', 'MO_TEC', 0.25, 0.1),
        ]
    },
    {
        'codigo': 'COMP_DRN_PVC',
        'descricao': 'Dreno tubo PVC 25mm',
        'desc_pre': 'Dreno tubo PVC 25mm com ',
        'desc_pos': '',
        'unid_sing': 'metro',
        'unid_plur': 'metros',
        'itens': [
            ('MAT', 'DRN_PVC_25', 0, 1.1),
            ('MAT', 'DRN_CURV_25', 2, 0),
            ('MAT', 'DRN_LUVA_25', 0, 0.5),
            ('MAT', 'DRN_COLA', 0.3, 0),
            ('MO', 'MO_TEC', 0.5, 0.15),
        ]
    },
    {
        'codigo': 'COMP_FURO',
        'descricao': 'Furo em parede/laje/viga (até 20cm espessura)',
        'itens': [
            ('MAT', 'ACA_ESPUMA', 0.2, 0),
            ('MAT', 'ACA_MASSA', 0.3, 0),
            ('MO', 'MO_TEC', 0.75, 0),
            ('MO', 'MO_AJU', 0.75, 0),
            ('FER', 'FER_PERF', 0.5, 0),
            ('FER', 'FER_SERRA_65', 1, 0),
        ]
    },
    {
        'codigo': 'COMP_CAN_50',
        'descricao': 'Acabamento canaleta PVC 50mm',
        'desc_pre': 'Acabamento canaleta PVC 50mm com ',
        'desc_pos': '',
        'unid_sing': 'metro',
        'unid_plur': 'metros',
        'itens': [
            ('MAT', 'ACA_CAN_50', 0, 1.1),
            ('MAT', 'SUP_BUCHA', 0, 2),
            ('MAT', 'SUP_CHIP', 0, 2),
            ('MO', 'MO_TEC', 0, 0.25),
        ]
    },
    {
        'codigo': 'COMP_ALV',
        'descricao': 'Abertura e fechamento alvenaria',
        'desc_pre': 'Abertura e fechamento alvenaria com ',
        'desc_pos': ' para embutir linha',
        'unid_sing': 'metro',
        'unid_plur': 'metros',
        'itens': [
            ('MAT', 'ALV_ARG', 0, 0.5),
            ('MAT', 'ALV_TIJ', 0, 10),
            ('MO', 'MO_PED', 1, 1.25),
            ('MO', 'MO_SERV', 1, 1.25),
            ('FER', 'FER_MANUAL', 1, 1),
        ]
    },
    {
        'codigo': 'COMP_FACH',
        'descricao': 'Instalação condensadora em fachada (com suporte)',
        'itens': [
            ('MAT', 'SUP_MF_500', 1, 0),
            ('MAT', 'SUP_PARF_150', 4, 0),
            ('MO', 'MO_TEC', 2, 0),
            ('MO', 'MO_AJU', 2, 0),
            ('MO', 'MO_FAC', 2, 0),
            ('FER', 'FER_PERF', 1, 0),
            ('FER', 'FER_MANUAL', 2, 0),
        ]
    },
    {
        'codigo': 'COMP_ALT',
        'descricao': 'Adicional trabalho em altura (acima 3m)',
        'itens': [
            ('MO', 'MO_ALT', 2, 0),
            ('FER', 'FER_ESCADA', 2, 0),
        ]
    },
    {
        'codigo': 'COMP_BOMB_DRN',
        'descricao': 'Instalação bomba de dreno',
        'itens': [
            ('EQP', 'EQP_BOMB_P', 1, 0),
            ('MAT', 'DRN_CRIS_34', 2, 0),
            ('MAT', 'ACA_FITA_ISO', 0.1, 0),
            ('MO', 'MO_TEC', 1, 0),
        ]
    },
    {
        'codigo': 'COMP_DISJ',
        'descricao': 'Instalação disjuntor no QDC',
        'itens': [
            ('MAT', 'DISJ_M_16', 1, 0),
            ('MAT', 'CAB_FLEX_25', 3, 0),
            ('MAT', 'ACA_FITA_ISO', 0.15, 0),
            ('MO', 'MO_ELE', 1, 0),
            ('FER', 'FER_MULT', 0.25, 0),
        ]
    },
    {
        'codigo': 'COMP_DRN_ESG',
        'descricao': 'Conexão dreno em rede esgoto (com sifão)',
        'itens': [
            ('MAT', 'DRN_PVC_25', 1, 0),
            ('MAT', 'DRN_SIFAO', 1, 0),
            ('MAT', 'DRN_CURV_25', 1, 0),
            ('MAT', 'DRN_COLA', 0.2, 0),
            ('MO', 'MO_TEC', 0.75, 0),
        ]
    },
    {
        'codigo': 'COMP_DESINST',
        'descricao': 'Desinstalação de equipamento Split',
        'itens': [
            ('MO', 'MO_TEC', 1.5, 0),
            ('MO', 'MO_AJU', 1.5, 0),
            ('FER', 'FER_MANIF', 0.5, 0),
            ('FER', 'FER_MANUAL', 1.5, 0),
        ]
    },
    {
        'codigo': 'COMP_GAS_ADIC',
        'descricao': 'Carga adicional gás R-410A (por kg)',
        'itens': [
            ('MAT', 'GAS_R410A', 1, 0),
            ('MO', 'MO_TEC', 0.5, 0),
            ('FER', 'FER_MANIF', 0.25, 0),
            ('FER', 'FER_BAL', 0.25, 0),
        ]
    },
]
