#!/usr/bin/env python3
"""
Script para configurar o projeto Asana de Orcamentos de Climatizacao
Cria as secoes, tags e tarefas de exemplo
"""

import json
import os
import sys

try:
    import requests
except ImportError:
    print("Instale o requests: pip install requests")
    sys.exit(1)


def load_config():
    """Carrega configuracao do arquivo JSON"""
    with open('asana-setup-config.json', 'r', encoding='utf-8') as f:
        return json.load(f)


def get_token():
    """Obtem o token do Asana"""
    token = os.environ.get('ASANA_ACCESS_TOKEN')
    if not token:
        token = input("Cole seu Asana Personal Access Token: ").strip()
    return token


def create_section(token, project_id, section_name):
    """Cria uma secao no projeto"""
    url = f"https://app.asana.com/api/1.0/projects/{project_id}/sections"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    data = {
        "data": {
            "name": section_name
        }
    }

    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 201:
        section_id = response.json()['data']['gid']
        print(f"✓ Secao criada: {section_name} (ID: {section_id})")
        return section_id
    else:
        print(f"✗ Erro ao criar secao {section_name}: {response.text}")
        return None


def create_tag(token, workspace_id, tag_name, color):
    """Cria uma tag no workspace"""
    url = "https://app.asana.com/api/1.0/tags"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    data = {
        "data": {
            "name": tag_name,
            "color": color,
            "workspace": workspace_id
        }
    }

    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 201:
        tag_id = response.json()['data']['gid']
        print(f"✓ Tag criada: {tag_name}")
        return tag_id
    else:
        # Tag pode ja existir
        print(f"⚠ Tag {tag_name}: {response.status_code}")
        return None


def create_task(token, project_id, section_id, task_data):
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
        return task_id
    else:
        print(f"✗ Erro ao criar tarefa: {response.text}")
        return None


def get_workspace_id(token):
    """Obtem o Workspace ID do usuario"""
    url = "https://app.asana.com/api/1.0/workspaces"
    headers = {
        "Authorization": f"Bearer {token}"
    }

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        workspaces = response.json()['data']
        if workspaces:
            workspace_id = workspaces[0]['gid']
            workspace_name = workspaces[0]['name']
            print(f"Workspace: {workspace_name} (ID: {workspace_id})")
            return workspace_id
    return None


def main():
    print("=" * 60)
    print("Configuracao do Projeto Asana - Orcamentos de Climatizacao")
    print("=" * 60)
    print()

    # Carregar configuracao
    config = load_config()
    project_id = config['project_id']
    print(f"Project ID: {project_id}")
    print()

    # Obter token
    token = get_token()

    # Obter workspace
    print("\n1. Obtendo Workspace...")
    workspace_id = get_workspace_id(token)
    if not workspace_id:
        print("✗ Erro ao obter Workspace")
        return

    # Criar secoes
    print(f"\n2. Criando {len(config['sections'])} secoes...")
    sections_map = {}
    for section in config['sections']:
        section_id = create_section(token, project_id, section['name'])
        if section_id:
            sections_map[section['name']] = section_id

    # Criar tags
    print(f"\n3. Criando {len(config['tags'])} tags...")
    tags_map = {}
    for tag in config['tags']:
        tag_id = create_tag(token, workspace_id, tag['name'], tag['color'])
        if tag_id:
            tags_map[tag['name']] = tag_id

    # Criar tarefas de exemplo
    print(f"\n4. Criando {len(config['example_tasks'])} tarefas de exemplo...")
    for task in config['example_tasks']:
        section_id = sections_map.get(task['section'])
        if section_id:
            create_task(token, project_id, section_id, task)

    print("\n" + "=" * 60)
    print("Configuracao concluida!")
    print("=" * 60)
    print(f"\nAcesse o projeto: https://app.asana.com/0/{project_id}")


if __name__ == "__main__":
    main()
