#!/usr/bin/env python3
"""
Script para criar exemplo de orcamento com subtarefas no Asana
Demonstra a abordagem 2 (subtarefas ao inves de secoes)
"""

import json
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
            "projects": [project_id],
            "due_on": task_data.get('due_on')
        }
    }

    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 201:
        task_id = response.json()['data']['gid']
        print(f"✓ Tarefa criada: {task_data['name']}")
        print(f"  ID: {task_id}")
        return task_id
    else:
        print(f"✗ Erro ao criar tarefa: {response.text}")
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
        subtask_id = response.json()['data']['gid']
        print(f"  ✓ Subtarefa criada: {subtask_data['name']}")
        return subtask_id
    else:
        print(f"  ✗ Erro ao criar subtarefa: {response.text}")
        return None


def main():
    print("=" * 70)
    print("Criar Orcamento Exemplo com Subtarefas")
    print("=" * 70)
    print()

    token = get_token()

    # Dados da tarefa principal
    tarefa_principal = {
        "name": "[INSTALACAO] Empresa ABC - Belo Horizonte (EXEMPLO SUBTAREFAS)",
        "due_on": "2025-02-15",
        "notes": """DADOS DO ORCAMENTO

Cliente: Empresa ABC Ltda
Contato: Joao Silva
Telefone: (31) 99999-8888
Email: joao@empresaabc.com.br
Local: Belo Horizonte - MG
Prazo do cliente: 15/02/2025

---

DETALHES DA DEMANDA
Instalacao de split 18.000 BTUs em sala de reunioes
- Distancia: ~8 metros
- Local condensadora: Laje externa
- Infraestrutura eletrica: Precisa adequacao
- Horario: Comercial

---

ORIGEM: Comercial
LICITACAO: Nao

---

CLASSIFICACAO
Tipo: Instalacao
Porte: Medio

---

OBSERVACOES
Cliente estrategico - priorizar qualidade no orcamento
"""
    }

    # Subtarefas (etapas do processo)
    subtarefas = [
        {
            "name": "📋 1. Triagem",
            "notes": """Avaliar:
- Viabilidade tecnica
- Prioridade (prazo, cliente, porte)
- Atribuir responsavel para elaboracao

Checklist:
[ ] Todas informacoes necessarias presentes?
[ ] Cliente estrategico?
[ ] Prazo urgente?
[ ] Definir responsavel pela elaboracao
"""
        },
        {
            "name": "✅ 2. Aprovacao para Elaboracao",
            "notes": """Confirmar que:
- Informacoes completas
- Responsavel atribuido
- Prazo viavel

Acao: Liberar para elaboracao
"""
        },
        {
            "name": "⚙️ 3. Elaboracao do Orcamento",
            "notes": """Criar orcamento completo:

Checklist:
[ ] Calcular materiais (equipamento, tubulacao, dreno, cabos)
[ ] Calcular mao de obra (instalacao, adequacao eletrica)
[ ] Definir prazo de execucao
[ ] Criar planilha orcamentaria
[ ] Revisar calculos
[ ] Formatar documento final
[ ] Anexar orcamento na tarefa

Responsavel: [Atribuir ao elaborador]
"""
        },
        {
            "name": "🔍 4. Revisao Interna",
            "notes": """Coordenador deve revisar:

Checklist:
[ ] Valores coerentes com mercado?
[ ] Margem adequada?
[ ] Condicoes comerciais ok?
[ ] Prazo de validade definido?
[ ] Documento formatado corretamente?
[ ] Informacoes do cliente corretas?

Acao: Aprovar ou solicitar ajustes
"""
        },
        {
            "name": "📤 5. Envio ao Cliente",
            "notes": """Enviar orcamento:

Checklist:
[ ] Enviar por email
[ ] Confirmar recebimento
[ ] Registrar data de envio
[ ] Agendar follow-up se necessario

Anexar: Comprovante de envio
"""
        },
        {
            "name": "🤝 6. Negociacao (se necessario)",
            "notes": """Registrar negociacoes:

Se cliente solicitar:
- Desconto
- Ajuste de escopo
- Mudanca de prazo
- Outras alteracoes

Acao: Tratar com coordenador e responder cliente

Nota: So completar esta etapa se houver negociacao
"""
        },
        {
            "name": "🏁 7. Fechamento",
            "notes": """Registrar resultado final:

Opcoes:
[ ] FECHADO - Valor: R$ _______
[ ] PERDIDO - Motivo: _______

Motivos de perda:
- Preco alto
- Prazo nao atendido
- Escolheu concorrente
- Cliente desistiu
- Nao conseguimos atender tecnicamente
- Outro: _______

Acao: Marcar tarefa como concluida e mover para "Concluido"
"""
        }
    ]

    # Criar tarefa principal
    print("1. Criando tarefa principal...")
    task_id = create_task(token, PROJECT_ID, tarefa_principal)

    if not task_id:
        print("\nErro ao criar tarefa principal. Abortando.")
        return

    print(f"\n2. Criando {len(subtarefas)} subtarefas...\n")

    # Criar subtarefas em ordem reversa (Asana adiciona no topo)
    for subtarefa in reversed(subtarefas):
        create_subtask(token, task_id, subtarefa)

    print("\n" + "=" * 70)
    print("Exemplo criado com sucesso!")
    print("=" * 70)
    print(f"\nAcesse a tarefa:")
    print(f"https://app.asana.com/0/{PROJECT_ID}/{task_id}")
    print("\nAbra a tarefa para ver todas as subtarefas (etapas do processo)")


if __name__ == "__main__":
    main()
