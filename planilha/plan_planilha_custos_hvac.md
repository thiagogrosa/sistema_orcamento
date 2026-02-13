📊 PLANO COMPLETO v3 - PLANILHA DE CUSTOS HVAC

1. ESTRUTURA GERAL DO ARQUIVO
AbaFunçãoINSTRUCOESManual de uso, lógica de nomenclaturas, como inserir novos itensPROMPTSPrompts para usar com LLM na criação de novos itensMATERIAISInsumos consumíveisMAO_DE_OBRAProfissionais e adicionaisFERRAMENTASFerramentas com custo/hora rateadoEQUIPAMENTOSSplits, bombas de dreno, etc.COMPOSICOESServiços com total na linha do códigoORCAMENTOMontagem de orçamentos completos

2. SISTEMA DE NOMENCLATURA (Proposta C - Híbrido)
2.1 Estrutura Geral dos Códigos
[CATEGORIA]_[ESPECIFICAÇÃO]_[QUALIFICADOR]
2.2 Tubulação de Cobre
Formato: TUB_[POLEGADA]_[TIPO]
TipoCódigoSignificadoFLEXFlexívelEspessura parede ~1/32" (0,79mm)RIGRígidoEspessura parede ~1/16" (1,58mm)
Lista de Códigos:
CódigoDescriçãoDiâmetroTipoTUB_14_FLEXTubo cobre 1/4" flexível6,35mmFlexívelTUB_38_FLEXTubo cobre 3/8" flexível9,52mmFlexívelTUB_12_FLEXTubo cobre 1/2" flexível12,70mmFlexívelTUB_58_FLEXTubo cobre 5/8" flexível15,87mmFlexívelTUB_58_RIGTubo cobre 5/8" rígido15,87mmRígidoTUB_34_FLEXTubo cobre 3/4" flexível19,05mmFlexívelTUB_34_RIGTubo cobre 3/4" rígido19,05mmRígidoTUB_78_RIGTubo cobre 7/8" rígido22,22mmRígidoTUB_118_RIGTubo cobre 1.1/8" rígido28,57mmRígidoTUB_138_RIGTubo cobre 1.3/8" rígido34,92mmRígido

2.3 Isolamento Térmico
Formato: ISO_[POLEGADA]_[TIPO]_[ESPESSURA]
TipoCódigoSignificadoELAElastoméricoArmaflex, K-Flex, similar (borracha)POLPolietilenoBlindado/revestido com alumínio
EspessuraCódigo9mmE910mmE1013mmE1319mmE1925mmE2532mmE32
Exemplos de Códigos:
CódigoDescriçãoISO_14_ELA_E9Isolamento elastomérico p/ 1/4", esp. 9mmISO_14_ELA_E13Isolamento elastomérico p/ 1/4", esp. 13mmISO_38_ELA_E9Isolamento elastomérico p/ 3/8", esp. 9mmISO_38_ELA_E13Isolamento elastomérico p/ 3/8", esp. 13mmISO_14_POL_E10Isolamento polietileno p/ 1/4", esp. 10mmISO_38_POL_E10Isolamento polietileno p/ 3/8", esp. 10mmISO_58_ELA_E19Isolamento elastomérico p/ 5/8", esp. 19mmISO_78_ELA_E19Isolamento elastomérico p/ 7/8", esp. 19mmISO_118_ELA_E25Isolamento elastomérico p/ 1.1/8", esp. 25mm

2.4 Cabos Elétricos
Formato: CAB_[TIPO]_[SEÇÃO]
CódigoDescriçãoCAB_PP_15Cabo PP 3x1,5mm²CAB_PP_25Cabo PP 3x2,5mm²CAB_PP_40Cabo PP 3x4mm²CAB_PP_60Cabo PP 3x6mm²CAB_FLEX_25Cabo flexível 2,5mm²CAB_FLEX_40Cabo flexível 4mm²CAB_FLEX_60Cabo flexível 6mm²CAB_COMCabo comunicação 2x0,75mm²

2.5 Eletrodutos e Conexões
Formato: COND_[TIPO]_[POLEGADA]
CódigoDescriçãoCOND_CORR_34Eletroduto corrugado 3/4"COND_CORR_100Eletroduto corrugado 1"COND_CURV_34Curva 90° eletroduto 3/4"COND_ABRC_34Abraçadeira eletroduto 3/4"

2.6 Dreno
Formato: DRN_[TIPO]_[ESPECIFICAÇÃO]
CódigoDescriçãoDRN_CRIS_34Mangueira cristal 3/4"DRN_CRIS_100Mangueira cristal 1"DRN_PVC_25Tubo PVC esgoto 25mmDRN_PVC_32Tubo PVC esgoto 32mmDRN_CURV_25Curva 90° PVC 25mmDRN_LUVA_25Luva PVC 25mmDRN_SIFAOSifão sanfonado universalDRN_COLACola PVCDRN_ABRCAbraçadeira nylon

2.7 Suportes e Fixação
Formato: SUP_[TIPO]_[ESPECIFICAÇÃO]
CódigoDescriçãoSUP_MF_400Suporte mão francesa 400mm (par)SUP_MF_500Suporte mão francesa 500mm (par)SUP_MF_600Suporte mão francesa 600mm (par)SUP_CALCOCalço borracha antivibração (jg 4pç)SUP_EVAPSuporte evaporadora universalSUP_PARF_100Parafuso sextavado 3/8"x100mm c/ buchaSUP_PARF_150Parafuso sextavado 3/8"x150mm c/ buchaSUP_BUCHABucha nylon S10SUP_CHIPParafuso chipboard 6x60mm

2.8 Acabamento
Formato: ACA_[TIPO]_[ESPECIFICAÇÃO]
CódigoDescriçãoACA_CAN_50Canaleta PVC 50x50mmACA_CAN_70Canaleta PVC 70x70mmACA_CAN_100Canaleta PVC 100x50mmACA_CURV_50Curva 90° canaleta 50mmACA_TAMP_50Tampa canaleta 50mmACA_ESPUMAEspuma expansiva 500mlACA_MASSAMassa de calafetar 400gACA_FITA_ISOFita isolante preta 20mACA_FITA_AUTFita autofusão 10mACA_FITA_TERFita isolante térmica 30m

2.9 Gás e Solda
Formato: GAS_[TIPO] / SOL_[TIPO]
CódigoDescriçãoGAS_R410AGás refrigerante R-410A (kg)GAS_R22Gás refrigerante R-22 (kg)GAS_R32Gás refrigerante R-32 (kg)GAS_N2Nitrogênio (carga teste)SOL_PRATAVareta solda prata 5%SOL_FLUXOFluxo para solda 100g

2.10 Proteção Elétrica
Formato: DISJ_[TIPO]_[AMPERAGEM]
CódigoDescriçãoDISJ_M_10Disjuntor monopolar 10ADISJ_M_16Disjuntor monopolar 16ADISJ_M_20Disjuntor monopolar 20ADISJ_B_20Disjuntor bipolar 20ADISJ_B_25Disjuntor bipolar 25ADISJ_B_32Disjuntor bipolar 32ADISJ_B_40Disjuntor bipolar 40ADISJ_CXCaixa sobrepor disjuntor

2.11 Alvenaria
Formato: ALV_[TIPO]
CódigoDescriçãoALV_ARGArgamassa pronta 20kgALV_TIJTijolo cerâmico 6 furosALV_GESSOGesso cola 5kg

2.12 Mão de Obra
Formato: MO_[FUNÇÃO]
CódigoDescriçãoUnidadeMO_TECTécnico em refrigeraçãoHMO_AJUAjudante de instalaçãoHMO_ELEEletricistaHMO_PEDPedreiroHMO_SERVServente de pedreiroHMO_ALTAdicional trabalho altura (>3m)HMO_FACAdicional trabalho fachadaHMO_DESL_20Deslocamento até 20kmVZMO_DESL_50Deslocamento 20-50kmVZ

2.13 Ferramentas
Formato: FER_[TIPO]
CódigoDescriçãoValor AquisiçãoVida Útil (H)FER_VACUOBomba de vácuoR$ 1.5002.000FER_MANIFManifold digitalR$ 8003.000FER_SOLDAKit solda oxigênio/GLPR$ 1.2001.500FER_PERFPerfuratriz/marteleteR$ 1.8002.500FER_SERRA_65Serra copo diamantada 65mmR$ 180150FER_SERRA_80Serra copo diamantada 80mmR$ 220150FER_ESCADAEscada extensível 6mR$ 8003.000FER_ANDAIMEAndaime cavalete (par)R$ 6002.000FER_ESTANQKit teste estanqueidadeR$ 3502.000FER_MULTMultímetro/alicate amperímetroR$ 4503.000FER_MANUALFerramentas manuais (conjunto)R$ 1.2004.000FER_FURADFuradeira de impactoR$ 6502.000FER_CORTACortador de tubo cobreR$ 1201.000FER_FLANGFlangeador/alargadorR$ 3802.000FER_BALBalança digital refrigeraçãoR$ 2802.500

2.14 Equipamentos
Formato: EQP_[TIPO]_[CAPACIDADE]
CódigoDescriçãoCapacidadeEQP_HW_9KSplit Hi-Wall Inverter 9.000 BTUs9.000EQP_HW_12KSplit Hi-Wall Inverter 12.000 BTUs12.000EQP_HW_18KSplit Hi-Wall Inverter 18.000 BTUs18.000EQP_HW_22KSplit Hi-Wall Inverter 22.000 BTUs22.000EQP_HW_24KSplit Hi-Wall Inverter 24.000 BTUs24.000EQP_HW_30KSplit Hi-Wall Inverter 30.000 BTUs30.000EQP_PT_36KSplit Piso-Teto 36.000 BTUs36.000EQP_PT_48KSplit Piso-Teto 48.000 BTUs48.000EQP_PT_60KSplit Piso-Teto 60.000 BTUs60.000EQP_BOMB_PBomba dreno mini (até 12k)-EQP_BOMB_MBomba dreno (até 36k)-EQP_BOMB_GBomba dreno (até 60k)-

2.15 Composições
Formato: COMP_[SERVIÇO]_[ESPECIFICAÇÃO]
CódigoDescriçãoCOMP_INST_9KInstalação Split 9.000 BTUs (3m linha + comunicação + fixação)COMP_MADC_9KMetro adicional linha frigorígena 9.000 BTUsCOMP_SUP_MFAdicional suporte mão francesa (condensadora)COMP_SUP_CALCOAdicional calços de borracha (condensadora)COMP_ELE_5MAlimentação elétrica 220V mono (5m cabo)COMP_ELE_ADICAdicional elétrica (por metro)COMP_DRN_CRISDreno mangueira cristal (3m)COMP_DRN_ADIC_CRISAdicional dreno mangueira (por metro)COMP_DRN_PVCDreno tubo PVC 25mm (3m)COMP_DRN_ADIC_PVCAdicional dreno PVC (por metro)COMP_FUROFuro em parede/laje/viga (até 20cm)COMP_CAN_50Acabamento canaleta PVC 50mm (por metro)COMP_ALV_3MAbertura e fechamento alvenaria (3m)COMP_ALV_ADICAdicional alvenaria (por metro)COMP_FACHInstalação condensadora em fachadaCOMP_ALTAdicional trabalho em altura (>3m)COMP_BOMB_DRNInstalação bomba de drenoCOMP_DISJInstalação disjuntor no QDCCOMP_DRN_ESGConexão dreno em rede esgoto (com sifão)COMP_DESINSTDesinstalação de equipamento SplitCOMP_GAS_ADICCarga adicional gás R-410A (por kg)

3. ESTRUTURA DAS ABAS
3.1 Aba INSTRUCOES
Seções:

Visão Geral - Explicação do propósito da planilha
Estrutura das Abas - O que contém cada aba
Sistema de Nomenclatura - Lógica completa dos códigos
Como Inserir Novos Itens - Passo a passo por tipo
Como Usar as Composições - Explicação das fórmulas
Como Montar um Orçamento - Uso da aba ORCAMENTO
Dicas e Boas Práticas - Recomendações gerais


3.2 Aba PROMPTS
Prompts para uso com LLM:
Prompt 1 - Criar Material
Você é um assistente especializado em HVAC. Preciso cadastrar um novo material na minha planilha de custos.

CONTEXTO DA NOMENCLATURA:
- Tubos: TUB_[POLEGADA]_[FLEX/RIG]
- Isolamentos: ISO_[POLEGADA]_[ELA/POL]_E[ESPESSURA_MM]
- Cabos: CAB_[TIPO]_[SEÇÃO]
- Dreno: DRN_[TIPO]_[ESPECIFICAÇÃO]
- Suportes: SUP_[TIPO]_[ESPECIFICAÇÃO]
- Acabamento: ACA_[TIPO]_[ESPECIFICAÇÃO]
- Gás: GAS_[TIPO] / Solda: SOL_[TIPO]
- Disjuntores: DISJ_[M/B]_[AMPERAGEM]
- Alvenaria: ALV_[TIPO]

MATERIAL A CADASTRAR: [DESCREVA O MATERIAL]

Responda com:
1. Código sugerido (seguindo a nomenclatura)
2. Categoria
3. Descrição completa
4. Unidade de medida
5. Preço estimado de mercado (Porto Alegre/RS)
Prompt 2 - Criar Mão de Obra
Você é um assistente especializado em HVAC. Preciso cadastrar uma nova função de mão de obra.

CONTEXTO DA NOMENCLATURA:
- Formato: MO_[FUNÇÃO]
- Exemplos: MO_TEC (técnico), MO_AJU (ajudante), MO_ELE (eletricista)

FUNÇÃO A CADASTRAR: [DESCREVA A FUNÇÃO]

Responda com:
1. Código sugerido
2. Categoria (Instalação, Elétrica, Civil, Adicional, Deslocamento)
3. Descrição completa
4. Unidade (H, VZ, DIA)
5. Custo estimado por unidade (Porto Alegre/RS)
Prompt 3 - Criar Ferramenta
Você é um assistente especializado em HVAC. Preciso cadastrar uma nova ferramenta com cálculo de depreciação.

CONTEXTO DA NOMENCLATURA:
- Formato: FER_[TIPO]
- Exemplos: FER_VACUO, FER_MANIF, FER_PERF

FERRAMENTA A CADASTRAR: [DESCREVA A FERRAMENTA]

Responda com:
1. Código sugerido
2. Categoria (Vácuo, Manifold, Solda, Furação, Acesso, Teste, Elétrica, Diversos)
3. Descrição completa
4. Valor de aquisição estimado (R$)
5. Vida útil estimada em HORAS de uso
6. Justificativa da vida útil
Prompt 4 - Criar Equipamento
Você é um assistente especializado em HVAC. Preciso cadastrar um novo equipamento de climatização.

CONTEXTO DA NOMENCLATURA:
- Splits Hi-Wall: EQP_HW_[CAPACIDADE]K
- Splits Piso-Teto: EQP_PT_[CAPACIDADE]K
- Cassete: EQP_CASS_[CAPACIDADE]K
- Bombas: EQP_BOMB_[P/M/G]

EQUIPAMENTO A CADASTRAR: [DESCREVA O EQUIPAMENTO]

Responda com:
1. Código sugerido
2. Categoria (Split Hi-Wall, Split Piso-Teto, Cassete, Bomba Dreno, etc.)
3. Descrição completa
4. Capacidade em BTUs (se aplicável)
5. Unidade (UN)
6. Preço estimado de mercado (Porto Alegre/RS)
Prompt 5 - Criar Composição
Você é um assistente especializado em HVAC. Preciso criar uma nova composição de serviço.

CONTEXTO DA NOMENCLATURA:
- Formato: COMP_[SERVIÇO]_[ESPECIFICAÇÃO]
- Exemplos: COMP_INST_9K, COMP_DRN_PVC, COMP_FURO

SERVIÇO A CRIAR: [DESCREVA O SERVIÇO]

Responda com:
1. Código sugerido
2. Descrição completa do serviço
3. Lista de insumos necessários (código, quantidade, unidade):
   - Materiais (MAT)
   - Mão de obra (MO)
   - Ferramentas (FER)
   - Equipamentos se aplicável (EQP)
4. Tempo estimado de execução
5. Observações técnicas importantes

3.3 Aba MATERIAIS
ColunaCampoFormatoACódigoTexto (ex: TUB_14_FLEX)BCategoriaTextoCDescriçãoTextoDUnidadeUN, M, KG, PAR, JG, SCEPreço (R$)Moeda

3.4 Aba MAO_DE_OBRA
ColunaCampoFormatoACódigoTexto (ex: MO_TEC)BCategoriaTextoCDescriçãoTextoDUnidadeH, VZ, DIAECusto (R$)Moeda

3.5 Aba FERRAMENTAS
ColunaCampoFormatoACódigoTexto (ex: FER_VACUO)BCategoriaTextoCDescriçãoTextoDValor Aquisição (R$)MoedaEVida Útil (H)NúmeroFCusto/Hora (R$)Fórmula =D/E

3.6 Aba EQUIPAMENTOS
ColunaCampoFormatoACódigoTexto (ex: EQP_HW_9K)BCategoriaTextoCDescriçãoTextoDCapacidade (BTU)Número ou "-"EUnidadeUNFPreço (R$)Moeda

3.7 Aba COMPOSICOES
Estrutura com TOTAL na linha do código:
ABCDEFGHCódigoDescriçãoTipoCód. ItemDescrição ItemUnQtdPreçoCOMP_INST_9KInstalação Split 9k...MATTUB_14_FLEX(PROCV)(PROCV)3,3(PROCV)MATTUB_38_FLEX(PROCV)(PROCV)3,3(PROCV)MOMO_TEC(PROCV)(PROCV)2,5(PROCV)FERFER_VACUO(PROCV)(PROCV)0,5(PROCV)
Fórmulas:

Coluna E (Descrição Item): =PROCV dinâmico baseado no TIPO
Coluna F (Unidade): =PROCV dinâmico baseado no TIPO
Coluna H (Preço): =PROCV dinâmico baseado no TIPO
Coluna I (Subtotal): =G*H
Coluna J (TOTAL): =SOMA() dos subtotais da composição

Validação de Dados:

Coluna C (Tipo): Dropdown com MAT, MO, FER, EQP
Coluna D (Cód. Item): Dropdown dinâmico baseado no TIPO selecionado (usando intervalos nomeados + INDIRETO)


3.8 Aba ORCAMENTO
Cabeçalho:

Cliente, Endereço
Data, Validade
Responsável, Telefone

Tabela de Itens:
ItemTipoCódigoDescriçãoQtdPreço Unit.Total1(dropdown)(dropdown dinâmico)(PROCV)(input)(PROCV)=Qtd*Preço
Tipos disponíveis: COMP, EQP, MAT, MO, FER
Totalizadores:

SUBTOTAL
DESCONTO (%)
TOTAL GERAL

Observações: Campo de texto livre

4. INTERVALOS NOMEADOS (para dropdowns dinâmicos)
NomeReferênciaUsoLISTA_MATMATERIAIS!A$2:
A$100
Dropdown códigos materiaisLISTA_MOMAO_DE_OBRA!A$2:
A$20
Dropdown códigos mão de obraLISTA_FERFERRAMENTAS!A$2:
A$30
Dropdown códigos ferramentasLISTA_EQPEQUIPAMENTOS!A$2:
A$30
Dropdown códigos equipamentosLISTA_COMPCOMPOSICOES!(códigos)Dropdown códigos composições

5. FORMATAÇÃO VISUAL
Cores por Tipo de Item (Composições)
TipoCor de FundoMATBrancoMOVerde claro (#EAFAF1)FERAmarelo claro (#FEF9E7)EQPAzul claro (#EBF5FB)
Cores por Categoria (Materiais)
CategoriaCorTubulaçãoAzul claro (#D6EAF8)IsolamentoVerde claro (#D5F5E3)ElétricaAmarelo claro (#FCF3CF)DrenoCiano (#D1F2EB)SuporteLaranja claro (#FAE5D3)AcabamentoRosa claro (#FADBD8)Gás/SoldaCinza (#E5E8E8)AlvenariaLilás (#F5EEF8)

6. CHECKLIST DE VALIDAÇÃO
Antes de executar, confirme:

 Sistema de nomenclatura está claro e completo?
 Categorias de cobre (FLEX/RIG) estão corretas?
 Categorias de isolamento (ELA/POL) e espessuras estão corretas?
 Lista de materiais está adequada?
 Lista de ferramentas com vida útil em horas está ok?
 Estrutura da aba INSTRUCOES está completa?
 Prompts para LLM estão úteis?
 Estrutura da aba ORCAMENTO atende?
 Algum código que ficou confuso ou faltou?


Me dá o OK ou ajustes que eu parto para a execução!Podemos seguir para a execução!13:35Architected comprehensive spreadsheet structure with eight specialized tabs.O usuário aprovou o plano completo. Agora preciso criar a planilha com todas as especificações detalhadas:

Aba INSTRUCOES - Manual de uso
Aba PROMPTS - Prompts para LLM
Aba MATERIAIS - Com nova nomenclatura
Aba MAO_DE_OBRA - Com nova nomenclatura
Aba FERRAMENTAS - Com custo/hora
Aba EQUIPAMENTOS - Splits e bombas
Aba COMPOSICOES - Com total na linha do código e dropdowns dinâmicos
Aba ORCAMENTO - Completa com cabeçalho e totalizadores
