#!/usr/bin/env python3
"""
Cria tarefa TEMPLATE/GUIA no Asana
Como o plano free nao permite templates, esta tarefa servira como
referencia para duplicar ao criar novos orcamentos
"""

import os
import sys

try:
    import requests
except ImportError:
    print("Instale: pip install requests")
    sys.exit(1)

# Tenta carregar do .env
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass  # dotenv opcional

PROJECT_ID = os.environ.get('ASANA_PROJECT_ID', "1212920325558530")


def get_token():
    """Obtem o token do Asana"""
    token = os.environ.get('ASANA_ACCESS_TOKEN')
    if not token:
        token = input("Cole seu Asana Personal Access Token: ").strip()
    return token


def create_task(token, project_id, task_data):
    """Cria uma tarefa no projeto"""
    url = "https://app.asana.com/api/1.0/tasks"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    data = {
        "data": {
            "name": task_data['name'],
            "notes": task_data['notes'],
            "projects": [project_id]
        }
    }

    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 201:
        task_id = response.json()['data']['gid']
        print(f"✓ Tarefa criada: {task_data['name']}")
        print(f"  ID: {task_id}")
        return task_id
    else:
        print(f"✗ Erro: {response.text}")
        return None


def create_subtask(token, parent_task_id, subtask_data):
    """Cria uma subtarefa"""
    url = f"https://app.asana.com/api/1.0/tasks/{parent_task_id}/subtasks"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    data = {
        "data": {
            "name": subtask_data['name'],
            "notes": subtask_data.get('notes', '')
        }
    }

    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 201:
        print(f"  ✓ Subtarefa: {subtask_data['name']}")
        return response.json()['data']['gid']
    else:
        print(f"  ✗ Erro: {response.text}")
        return None


def main():
    print("=" * 70)
    print("Criar Tarefa TEMPLATE/GUIA - Orcamentos")
    print("=" * 70)
    print()

    token = get_token()

    # Tarefa principal - TEMPLATE
    template = {
        "name": "🔖 TEMPLATE - Como criar um orcamento (DUPLICAR ESTA TAREFA)",
        "notes": """═══════════════════════════════════════════════════════════════════
📋 COMO USAR ESTE TEMPLATE
═══════════════════════════════════════════════════════════════════

1. DUPLICAR esta tarefa (nao mover, nao editar)
2. Renomear a copia com: [TIPO] Cliente - Local
3. Preencher os campos abaixo com dados reais
4. Marcar as subtarefas conforme o processo avanca
5. Nunca deletar ou editar este TEMPLATE original

═══════════════════════════════════════════════════════════════════
📝 TEMPLATE DE PREENCHIMENTO
═══════════════════════════════════════════════════════════════════

DADOS DO ORCAMENTO

Cliente: [Nome da empresa ou pessoa]
CNPJ/CPF: [Documento do cliente]
Contato: [Nome da pessoa de contato]
Telefone: [(XX) XXXXX-XXXX]
Email: [email@cliente.com.br]
Endereco: [Rua, Numero - Bairro - Cidade/UF - CEP]
Local do Servico: [Se diferente do endereco, informar onde sera executado]

Prazo do cliente: [DD/MM/AAAA]

---

DETALHES DA DEMANDA

[Descrever em detalhes o que o cliente solicitou]

Para INSTALACAO, incluir:
- Tipo e capacidade do equipamento
- Local de instalacao (ambiente)
- Distancia evaporadora/condensadora
- Local da condensadora
- Necessidade de suporte
- Infraestrutura eletrica (existe? precisa adequacao?)
- Servicos complementares (dreno, furos, canaleta, civil, gesso, etc.)
- Horario de execucao (comercial/fora)
- Acesso ao local

Para MANUTENCAO, incluir:
- Tipo (preventiva/corretiva)
- Quantidade de equipamentos
- Marca, modelo e capacidade de cada
- Localizacao dos equipamentos
- Problema relatado (se corretiva)
- Frequencia desejada (se contrato)

Para PROJETO, incluir:
- Tipo de projeto (basico/executivo/conceitual)
- Atividade do local (hospital, escritorio, industria, etc.)
- Normas aplicaveis
- Anexar plantas/desenhos

---

ORIGEM DA DEMANDA

[ ] Comercial/Vendas
[ ] Cliente direto
[ ] Diretoria
[ ] Engenharia

LICITACAO?
[ ] Sim - Numero/Edital: _______________
[ ] Nao

---

CLASSIFICACAO

Tipo: [Instalacao / Manutencao / Projeto]
Porte: [Pequeno / Medio / Grande]
Prioridade: [Normal / Urgente / Cliente Estrategico]

---

OBSERVACOES IMPORTANTES

[Qualquer informacao adicional relevante]

═══════════════════════════════════════════════════════════════════
📌 INSTRUCOES DAS SUBTAREFAS (ETAPAS DO PROCESSO)
═══════════════════════════════════════════════════════════════════

Cada subtarefa representa uma etapa do processo de orcamentacao.
Marque como concluida conforme avanca.
O Asana registrara automaticamente: quem completou, quando, e quanto tempo levou.

Veja as instrucoes detalhadas de cada etapa nas subtarefas abaixo.
"""
    }

    # Subtarefas (em ordem reversa pois Asana adiciona no topo)
    subtarefas = [
        {
            "name": "🏁 7. Fechamento",
            "notes": """═══════════════════════════════════════════════════════════════════
ETAPA 7: FECHAMENTO
═══════════════════════════════════════════════════════════════════

OBJETIVO: Registrar o resultado final do orcamento

RESPONSAVEL: Coordenador

---

CHECKLIST:

[ ] Confirmar decisao do cliente
[ ] Registrar resultado abaixo
[ ] Se fechado: registrar valor do contrato
[ ] Se perdido: registrar motivo
[ ] Mover tarefa principal para secao "Concluido"
[ ] Marcar esta subtarefa como concluida

---

RESULTADO:

OPCAO 1 - FECHADO ✅
Valor do contrato: R$ _______________
Data de fechamento: ___/___/______
Previsao de execucao: ___/___/______
Observacoes: _____________________

OPCAO 2 - PERDIDO ❌
Motivo da perda:
[ ] Preco alto
[ ] Prazo nao atendido
[ ] Escolheu concorrente
[ ] Cliente desistiu do projeto
[ ] Nao conseguimos atender tecnicamente
[ ] Outro: _______________________

Detalhes: _______________________

---

METRICAS (automaticas pelo Asana):
- Data de conclusao desta etapa
- Tempo total do orcamento (criacao ate fechamento)
"""
        },
        {
            "name": "🤝 6. Negociacao (se necessario)",
            "notes": """═══════════════════════════════════════════════════════════════════
ETAPA 6: NEGOCIACAO (OPCIONAL)
═══════════════════════════════════════════════════════════════════

OBJETIVO: Tratar solicitacoes de ajustes do cliente

RESPONSAVEL: Coordenador ou Elaborador (conforme complexidade)

QUANDO USAR: Apenas se o cliente solicitar ajustes

---

TIPOS DE NEGOCIACAO:

1. DESCONTO
   - Avaliar margem disponivel
   - Definir limite de desconto
   - Solicitar aprovacao se necessario

2. AJUSTE DE ESCOPO
   - Revisar itens solicitados
   - Recalcular orcamento
   - Gerar nova versao

3. MUDANCA DE PRAZO
   - Avaliar viabilidade
   - Ajustar cronograma
   - Atualizar orcamento

4. OUTRAS ALTERACOES
   - Avaliar impacto
   - Definir com coordenador
   - Formalizar mudancas

---

CHECKLIST:

[ ] Receber solicitacao do cliente
[ ] Avaliar viabilidade
[ ] Calcular impacto (custo, prazo, margem)
[ ] Obter aprovacao interna se necessario
[ ] Gerar nova versao do orcamento
[ ] Enviar resposta ao cliente
[ ] Registrar negociacao nos comentarios
[ ] Aguardar decisao final do cliente
[ ] Marcar como concluida quando cliente decidir

---

IMPORTANTE:
- Se nao houver negociacao, pule esta etapa
- Registre todas as versoes do orcamento
- Mantenha historico de todas as propostas
"""
        },
        {
            "name": "📤 5. Envio ao Cliente",
            "notes": """═══════════════════════════════════════════════════════════════════
ETAPA 5: ENVIO AO CLIENTE
═══════════════════════════════════════════════════════════════════

OBJETIVO: Enviar orcamento aprovado ao cliente

RESPONSAVEL: Elaborador ou Coordenador

---

CHECKLIST ANTES DE ENVIAR:

[ ] Orcamento aprovado na revisao interna
[ ] Documento formatado corretamente
[ ] Informacoes do cliente corretas
[ ] Prazo de validade definido
[ ] Condicoes comerciais claras
[ ] Anexos necessarios incluidos

---

PROCESSO DE ENVIO:

[ ] Redigir email de envio
[ ] Anexar orcamento em PDF
[ ] Anexar documentos complementares (se houver)
[ ] Enviar para o email do cliente
[ ] Copiar coordenador (cc)
[ ] Confirmar recebimento

---

MODELO DE EMAIL:

Assunto: Orcamento [Numero] - [Nome do Cliente]

Prezado [Nome],

Conforme solicitado, segue em anexo nossa proposta comercial para [tipo de servico].

Detalhes:
- Objeto: [descricao resumida]
- Prazo de validade: [dias] dias
- Prazo de execucao: [prazo]

Estamos a disposicao para esclarecimentos.

Att,
[Seu nome]
[Setor de Orcamentos]

---

POS-ENVIO:

[ ] Registrar data de envio
[ ] Agendar follow-up (se necessario)
[ ] Anexar comprovante de envio
[ ] Marcar esta subtarefa como concluida

---

OBSERVACAO: Data de conclusao desta subtarefa = Data de envio
"""
        },
        {
            "name": "🔍 4. Revisao Interna",
            "notes": """═══════════════════════════════════════════════════════════════════
ETAPA 4: REVISAO INTERNA
═══════════════════════════════════════════════════════════════════

OBJETIVO: Revisar e aprovar orcamento antes do envio ao cliente

RESPONSAVEL: Coordenador

---

CHECKLIST DE REVISAO:

VALORES E CALCULOS:
[ ] Valores coerentes com mercado
[ ] Margem de lucro adequada
[ ] Descontos dentro da politica
[ ] Custos bem dimensionados
[ ] Impostos incluidos

CONDICOES COMERCIAIS:
[ ] Forma de pagamento definida
[ ] Prazo de validade claro
[ ] Prazo de execucao realista
[ ] Garantias especificadas
[ ] Reajustes previstos (se aplicavel)

DOCUMENTACAO:
[ ] Documento formatado corretamente
[ ] Logo e cabecalho da empresa
[ ] Informacoes do cliente corretas
[ ] Escopo bem descrito
[ ] Observacoes e exclusoes claras

TECNICO:
[ ] Especificacoes tecnicas corretas
[ ] Normas aplicaveis atendidas
[ ] Prazos viaveis
[ ] Recursos disponiveis

---

ACOES:

SE APROVADO:
[ ] Adicionar comentario: "Aprovado para envio"
[ ] Marcar esta subtarefa como concluida
[ ] Seguir para proxima etapa

SE PRECISA AJUSTES:
[ ] Listar ajustes necessarios nos comentarios
[ ] Marcar subtarefa "3. Elaboracao" como nao concluida
[ ] Notificar elaborador
[ ] Aguardar correcoes

---

CRITERIOS DE APROVACAO:
- Margem minima: [definir %]
- Prazo maximo de validade: [definir dias]
- Alçadas de aprovacao: [definir valores]
"""
        },
        {
            "name": "⚙️ 3. Elaboracao do Orcamento",
            "notes": """═══════════════════════════════════════════════════════════════════
ETAPA 3: ELABORACAO DO ORCAMENTO
═══════════════════════════════════════════════════════════════════

OBJETIVO: Criar orcamento completo e detalhado

RESPONSAVEL: [Atribuir ao elaborador - Junior/Pleno/Senior conforme complexidade]

---

CHECKLIST GERAL:

LEVANTAMENTO:
[ ] Revisar todas informacoes da demanda
[ ] Confirmar dados com cliente se necessario
[ ] Identificar fornecedores
[ ] Solicitar cotacoes de materiais
[ ] Calcular mao de obra necessaria

CALCULO:
[ ] Listar todos os materiais necessarios
[ ] Calcular quantidades
[ ] Obter precos atualizados
[ ] Calcular horas de mao de obra
[ ] Incluir custos indiretos
[ ] Aplicar impostos
[ ] Definir margem de lucro
[ ] Calcular preco final

DOCUMENTACAO:
[ ] Criar planilha orcamentaria
[ ] Detalhar itens e quantidades
[ ] Especificar marcas e modelos
[ ] Definir prazo de execucao
[ ] Definir prazo de validade
[ ] Definir condicoes de pagamento
[ ] Incluir observacoes e exclusoes
[ ] Formatar documento final
[ ] Revisar calculos
[ ] Anexar orcamento na tarefa

---

CHECKLIST ESPECIFICO POR TIPO:

INSTALACAO:
[ ] Especificar equipamento (marca, modelo, capacidade)
[ ] Calcular tubulacao necessaria
[ ] Prever materiais eletricos
[ ] Incluir suportes e fixacoes
[ ] Prever servicos complementares (dreno, furos, acabamentos)
[ ] Calcular horas de instalacao
[ ] Incluir transporte se necessario

MANUTENCAO:
[ ] Definir escopo (preventiva/corretiva)
[ ] Listar equipamentos
[ ] Prever pecas de reposicao
[ ] Calcular mao de obra
[ ] Definir frequencia (se contrato)
[ ] Incluir deslocamento

PROJETO:
[ ] Definir tipo de projeto (basico/executivo)
[ ] Calcular horas de engenharia
[ ] Prever memorias de calculo
[ ] Incluir ART/TRT
[ ] Definir entregas

---

ARQUIVOS A ANEXAR:
- Planilha orcamentaria (Excel/PDF)
- Cotacoes de fornecedores
- Especificacoes tecnicas
- Plantas/desenhos (se projeto)

---

PRAZO ESPERADO:
- Pequeno porte: [X] dias
- Medio porte: [Y] dias
- Grande porte: [Z] dias
- Licitacao: [W] dias

---

AO CONCLUIR:
[ ] Anexar todos os arquivos
[ ] Adicionar comentario resumindo o orcamento
[ ] Marcar esta subtarefa como concluida
[ ] Notificar coordenador para revisao
"""
        },
        {
            "name": "✅ 2. Aprovacao para Elaboracao",
            "notes": """═══════════════════════════════════════════════════════════════════
ETAPA 2: APROVACAO PARA ELABORACAO
═══════════════════════════════════════════════════════════════════

OBJETIVO: Confirmar que orcamento esta pronto para ser elaborado

RESPONSAVEL: Coordenador

---

CHECKLIST:

[ ] Triagem concluida
[ ] Orcamento viavel tecnicamente
[ ] Todas informacoes necessarias presentes
[ ] Responsavel pela elaboracao definido
[ ] Prazo viavel
[ ] Prioridade definida

---

VALIDACOES:

INFORMACOES COMPLETAS?
- Dados do cliente completos
- Contato definido
- Escopo claro
- Local de execucao definido
- Prazo do cliente informado
- Informacoes tecnicas suficientes

RECURSOS DISPONIVEIS?
- Equipe disponivel para elaborar
- Prazo suficiente
- Fornecedores disponiveis (se necessario)

---

ACOES:

SE TUDO OK:
[ ] Atribuir subtarefa "3. Elaboracao" ao responsavel
[ ] Definir prazo para elaboracao
[ ] Marcar esta subtarefa como concluida
[ ] Notificar elaborador

SE FALTAM INFORMACOES:
[ ] Listar informacoes faltantes nos comentarios
[ ] Solicitar complemento ao solicitante
[ ] Manter esta subtarefa pendente
[ ] Aguardar retorno

SE NAO VIAVEL:
[ ] Justificar motivo nos comentarios
[ ] Notificar solicitante
[ ] Pular para subtarefa "7. Fechamento" e marcar como "perdido"
"""
        },
        {
            "name": "📋 1. Triagem",
            "notes": """═══════════════════════════════════════════════════════════════════
ETAPA 1: TRIAGEM
═══════════════════════════════════════════════════════════════════

OBJETIVO: Avaliar viabilidade e definir prioridade do orcamento

RESPONSAVEL: Coordenador

PRAZO: Ate 1 dia util apos criacao da demanda

---

CHECKLIST DE TRIAGEM:

VIABILIDADE TECNICA:
[ ] Conseguimos executar este servico?
[ ] Temos equipe/capacidade?
[ ] Temos conhecimento tecnico necessario?
[ ] Precisamos de parceiros/terceiros?

VIABILIDADE COMERCIAL:
[ ] Prazo do cliente e viavel?
[ ] Cliente tem perfil adequado?
[ ] Valor potencial justifica o esforco?
[ ] Regiao de atendimento?

INFORMACOES:
[ ] Dados do cliente completos?
[ ] Escopo bem definido?
[ ] Informacoes tecnicas suficientes?
[ ] Contato disponivel para duvidas?

---

PRIORIZACAO:

CRITERIOS DE PRIORIDADE:
1. Prazo urgente (< 3 dias)
2. Cliente estrategico
3. Alto valor potencial
4. Licitacao com prazo
5. Ordem de chegada

CLASSIFICACAO:
[ ] URGENTE - Iniciar imediatamente
[ ] ALTA - Iniciar em 1-2 dias
[ ] MEDIA - Fila normal
[ ] BAIXA - Quando houver disponibilidade

---

ATRIBUICAO POR COMPLEXIDADE:

[ ] SIMPLES - Novo funcionario (junior)
    - Pequeno porte
    - Servico padrao
    - Sem especificidades

[ ] MEDIA - Funcionario experiente (pleno)
    - Medio porte
    - Algumas especificidades
    - Cliente conhecido

[ ] COMPLEXA - Senior/Coordenador
    - Grande porte
    - Licitacao
    - Cliente estrategico
    - Prazo apertado
    - Tecnologia diferenciada

---

ACOES APOS TRIAGEM:

SE VIAVEL:
[ ] Definir responsavel pela elaboracao
[ ] Definir prioridade
[ ] Adicionar tags apropriadas
[ ] Marcar esta subtarefa como concluida
[ ] Seguir para proxima etapa

SE NAO VIAVEL:
[ ] Justificar motivo nos comentarios
[ ] Notificar solicitante
[ ] Pular para etapa 7 (Fechamento) e marcar como "perdido"

SE FALTAM INFORMACOES:
[ ] Listar o que falta nos comentarios
[ ] Solicitar ao cliente/solicitante
[ ] Manter esta subtarefa pendente ate receber

---

TEMPO ESPERADO NESTA ETAPA: 30 minutos a 2 horas
"""
        }
    ]

    print("1. Criando tarefa TEMPLATE...")
    task_id = create_task(token, PROJECT_ID, template)

    if not task_id:
        print("\nErro ao criar template.")
        return

    print(f"\n2. Criando {len(subtarefas)} subtarefas...\n")

    # Criar em ordem reversa (Asana adiciona no topo)
    for subtarefa in reversed(subtarefas):
        create_subtask(token, task_id, subtarefa)

    print("\n" + "=" * 70)
    print("Template/Guia criado com sucesso!")
    print("=" * 70)
    print(f"\nAcesse: https://app.asana.com/0/{PROJECT_ID}/{task_id}")
    print("\nUSO: Sempre DUPLICAR esta tarefa ao criar novo orcamento")


if __name__ == "__main__":
    main()
