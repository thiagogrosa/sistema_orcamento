#!/usr/bin/env python3
"""
Gerador de PDF da Proposta Comercial HVAC

Gera PDF estilizado a partir do orcamento precificado.
Usa template HTML + CSS e converte para PDF via weasyprint.
"""

import base64
from datetime import date, datetime
from pathlib import Path
from typing import Dict, Any, Optional, List

from jinja2 import Environment, FileSystemLoader, select_autoescape

from .utils import (
    carregar_configs,
    proximo_numero_orcamento,
    detectar_revisao,
    formatar_moeda,
    formatar_numero,
    valor_por_extenso,
    data_por_extenso,
    obter_exclusoes,
    obter_condicoes,
    criar_pasta_cliente,
    gerar_nome_arquivo,
    BASE_DIR
)


def carregar_logo_base64(logo_path: str) -> Optional[str]:
    """Carrega logo como base64 para embedar no HTML"""
    full_path = BASE_DIR / logo_path
    if full_path.exists():
        with open(full_path, "rb") as f:
            return base64.b64encode(f.read()).decode("utf-8")
    return None


def preparar_grupos(precificado: Dict[str, Any]) -> List[Dict]:
    """
    Prepara dados dos grupos/itens para o template

    Args:
        precificado: Dados do orcamento precificado

    Returns:
        Lista de grupos com itens formatados
    """
    grupos = []
    itens = precificado.get("itens_precificados", [])
    agrupamento = precificado.get("agrupamento", [])

    # Se tem agrupamento definido, usa
    if agrupamento:
        for idx, grupo in enumerate(agrupamento, 1):
            grupo_itens = []
            subtotal = 0

            for item_id in grupo.get("itens_ids", []):
                # Busca item pelo id
                for item in itens:
                    if item.get("id") == item_id:
                        valor_total = item.get("preco_total", 0)
                        quantidade = item.get("quantidade", 1)
                        valor_unit = valor_total / quantidade if quantidade > 0 else 0

                        grupo_itens.append({
                            "descricao": item.get("descricao", ""),
                            "unidade": item.get("unidade", "pc"),
                            "quantidade": quantidade,
                            "valor_unitario": valor_unit,
                            "valor_total": valor_total
                        })
                        subtotal += valor_total
                        break

            grupos.append({
                "numero": idx,
                "nome": grupo.get("nome", f"GRUPO {idx}"),
                "itens": grupo_itens,
                "subtotal": subtotal
            })
    else:
        # Sem agrupamento - cria grupo unico
        grupo_itens = []
        subtotal = 0

        for item in itens:
            valor_total = item.get("preco_total", 0)
            quantidade = item.get("quantidade", 1)
            valor_unit = valor_total / quantidade if quantidade > 0 else 0

            grupo_itens.append({
                "descricao": item.get("descricao", ""),
                "unidade": item.get("unidade", "pc"),
                "quantidade": quantidade,
                "valor_unitario": valor_unit,
                "valor_total": valor_total
            })
            subtotal += valor_total

        grupos.append({
            "numero": 1,
            "nome": "SERVICOS",
            "itens": grupo_itens,
            "subtotal": subtotal
        })

    return grupos


def detectar_tipo_servico(precificado: Dict[str, Any]) -> str:
    """Detecta o tipo de servico predominante"""
    itens = precificado.get("itens_precificados", [])

    tipos = {}
    for item in itens:
        tipo = item.get("tipo_servico", "instalacao")
        tipos[tipo] = tipos.get(tipo, 0) + 1

    if tipos:
        return max(tipos, key=tipos.get)
    return "instalacao"


def gerar_proposta_pdf(
    precificado: Dict[str, Any],
    rascunho: bool = False,
    numero_orcamento: Optional[str] = None,
    revisao: Optional[str] = None,
    output_path: Optional[str] = None,
    configs: Optional[Dict] = None
) -> Dict[str, Any]:
    """
    Gera PDF da proposta comercial

    Args:
        precificado: Dados do orcamento precificado
        rascunho: Se True, adiciona marca d'agua RASCUNHO
        numero_orcamento: Numero do orcamento (gera automatico se nao informado)
        revisao: Numero da revisao (ex: "R01"). Se nao informado, detecta automatico.
        output_path: Caminho de saida (gera automatico se nao informado)
        configs: Configuracoes (carrega se nao informado)

    Returns:
        Dicionario com resultado:
        {
            "sucesso": bool,
            "numero_orcamento": str,
            "arquivo_pdf": str,
            "arquivo_rascunho": str (se rascunho=True),
            "erro": str (se falhou)
        }
    """
    try:
        # Importa weasyprint aqui para nao falhar se nao estiver instalado
        from weasyprint import HTML, CSS
    except ImportError:
        return {
            "sucesso": False,
            "erro": "weasyprint nao instalado. Execute: pip install weasyprint"
        }

    # Carrega configs
    if configs is None:
        configs = carregar_configs()

    empresa = configs.get("empresa", {})
    usuario = configs.get("usuario", {})

    # Dados do cliente
    dados_cliente = precificado.get("dados_cliente", {})
    cliente_nome_bruto = dados_cliente.get("razao_social") or precificado.get("cliente", "Cliente")
    cliente_nome = cliente_nome_bruto.title() # Formata para Title Case
    tipo_cliente = precificado.get("tipo_cliente", "PRIVADO-PJ")

    # Determina numero e revisao
    cliente_dir = criar_pasta_cliente(cliente_nome_bruto) # Mantem nome bruto para pasta para consistencia

    # 1. Se numero nao informado, gera proximo
    if numero_orcamento is None:
        numero_base, _ = proximo_numero_orcamento(configs)
        # Remove a revisao padrao do gerador (-R00) para recalcular
        numero_base = numero_base.split("-R")[0]
    else:
        # Se informado manualmente, usa ele
        numero_base = numero_orcamento.split("-R")[0]
        
        # Se o numero manual ja tiver revisao e revisao nao foi passada explicita, usa a do numero
        if "-R" in numero_orcamento and revisao is None:
            revisao = "R" + numero_orcamento.split("-R")[1]

    # 2. Se revisao nao informada, detecta automatica
    if revisao is None:
        revisao_sufixo, _ = detectar_revisao(cliente_nome_bruto, cliente_dir)
        revisao = revisao_sufixo
    else:
        # Formata revisao se necessario (ex: "1" -> "R01")
        if not revisao.startswith("R"):
            try:
                val = int(revisao)
                revisao = f"R{val:02d}"
            except ValueError:
                if not revisao.startswith("R"):
                    revisao = f"R{revisao}"

    # 3. Monta numero final
    numero_orcamento = f"{numero_base}-{revisao}"

    # Prepara dados para template
    grupos = preparar_grupos(precificado)
    valor_total = sum(g["subtotal"] for g in grupos)
    tipo_servico = detectar_tipo_servico(precificado)

    # Verifica se precisa mostrar coluna unitario
    mostrar_unitario = any(
        item["quantidade"] > 1
        for grupo in grupos
        for item in grupo["itens"]
    )

    # Condicoes comerciais
    condicoes = obter_condicoes(tipo_cliente, configs)

    # Sobrescreve com customizacoes
    opcoes = precificado.get("opcoes_output", {})
    condicoes_custom = opcoes.get("condicoes_customizadas", {})
    condicoes.update(condicoes_custom)

    # Exclusoes
    exclusoes = obter_exclusoes(tipo_servico, configs)

    # Carrega logo
    logo_base64 = carregar_logo_base64(empresa.get("logo_path", ""))
    
    # Carrega logos adicionais e marca d'agua
    logo_abrava_base64 = carregar_logo_base64("templates/html/abrava_2025.png")
    logo_asbrav_base64 = carregar_logo_base64("templates/html/asbrav_2025.png")
    logo_secundario_base64 = carregar_logo_base64("templates/html/logo_secundario.png")
    marca_dagua_base64 = carregar_logo_base64("templates/html/helice_armant.png")

    # Carrega assinaturas com base64
    assinaturas = []
    for ass in empresa.get("assinaturas", []):
        ass_copia = ass.copy()
        img_path = ass.get("assinatura_img")
        if img_path:
            ass_copia["assinatura_img_base64"] = carregar_logo_base64(img_path)
        assinaturas.append(ass_copia)

    # Força data atual conforme solicitado
    data_hoje = date.today()

    # Monta contexto do template
    contexto = {
        "numero_orcamento": numero_orcamento,
        "cidade": empresa.get("endereco", {}).get("cidade", "Porto Alegre"),
        "data_extenso": data_por_extenso(data_hoje),
        "cliente": {
            "razao_social": cliente_nome, # Nome formatado
            "cnpj": dados_cliente.get("cnpj"),
            "cpf": dados_cliente.get("cpf"),
            "endereco": dados_cliente.get("endereco", ""),
            "contato_nome": dados_cliente.get("contato_nome", ""),
            "contato_email": dados_cliente.get("contato_email", ""),
            "contato_telefone": dados_cliente.get("contato_telefone", "")
        },
        "referencia": precificado.get("referencia") or precificado.get("projeto", "Serviços de Climatização"),
        "grupos": grupos,
        "mostrar_unitario": mostrar_unitario,
        "valor_total": valor_total,
        "valor_extenso": valor_por_extenso(valor_total),
        "destaques": empresa.get("destaques", []),
        "responsavel": usuario,
        "exclusoes": exclusoes,
        "observacoes": precificado.get("observacoes"),
        "condicoes": condicoes,
        "assinaturas": assinaturas,
        "empresa": empresa,
        "logo_base64": logo_base64,
        "logo_secundario_base64": logo_secundario_base64,
        "logo_abrava_base64": logo_abrava_base64,
        "logo_asbrav_base64": logo_asbrav_base64,
        "marca_dagua_base64": marca_dagua_base64,
        "rascunho": False # Sempre gera o principal limpo primeiro
    }

    # Configura Jinja2
    template_dir = BASE_DIR / "templates" / "html"
    env = Environment(
        loader=FileSystemLoader(template_dir),
        autoescape=select_autoescape(["html", "xml"])
    )

    # Adiciona filtros customizados
    env.filters["formatar_moeda"] = formatar_moeda
    env.filters["formatar_numero"] = formatar_numero

    # Carrega e renderiza template
    template = env.get_template("proposta_base.html")
    html_content = template.render(**contexto)

    # Carrega CSS
    css_path = template_dir / "proposta_styles.css"
    css_content = ""
    if css_path.exists():
        with open(css_path, "r", encoding="utf-8") as f:
            css_content = f.read()

    # Gera nome do arquivo
    nome_arquivo = gerar_nome_arquivo(
        numero_orcamento,
        cliente_nome,
        tipo_servico,
        revisao
    )

    # Define caminho de saida
    if output_path is None:
        output_path = cliente_dir / f"{nome_arquivo}.pdf"
    else:
        output_path = Path(output_path)

    output_path.parent.mkdir(parents=True, exist_ok=True)

    # Gera PDF
    html = HTML(string=html_content, base_url=str(template_dir))
    css = CSS(string=css_content)
    html.write_pdf(str(output_path), stylesheets=[css])

    resultado = {
        "sucesso": True,
        "numero_orcamento": numero_orcamento,
        "arquivo_pdf": str(output_path),
        "valor_total": valor_total
    }

    # Gera versao rascunho se solicitado
    if rascunho:
        contexto["rascunho"] = True
        html_rascunho = template.render(**contexto)

        rascunho_path = output_path.parent / f"{nome_arquivo}_RASCUNHO.pdf"
        html_rasc = HTML(string=html_rascunho, base_url=str(template_dir))
        html_rasc.write_pdf(str(rascunho_path), stylesheets=[css])

        resultado["arquivo_rascunho"] = str(rascunho_path)

    return resultado


def main():
    """CLI para teste"""
    import argparse
    import json

    parser = argparse.ArgumentParser(description="Gera PDF da proposta comercial")
    parser.add_argument("--input", "-i", required=True, help="Arquivo precificado.json")
    parser.add_argument("--output", "-o", help="Arquivo PDF de saida")
    parser.add_argument("--rascunho", action="store_true", help="Gera versao rascunho")
    parser.add_argument("--numero", "-n", help="Numero do orcamento (ex: 2026/001)")
    parser.add_argument("--revisao", "-r", help="Numero da revisao (ex: R01 ou 1)")

    args = parser.parse_args()

    with open(args.input, "r", encoding="utf-8") as f:
        precificado = json.load(f)

    resultado = gerar_proposta_pdf(
        precificado,
        rascunho=args.rascunho,
        numero_orcamento=args.numero,
        revisao=args.revisao,
        output_path=args.output
    )

    if resultado["sucesso"]:
        print(f"PDF gerado: {resultado['arquivo_pdf']}")
        if resultado.get("arquivo_rascunho"):
            print(f"Rascunho: {resultado['arquivo_rascunho']}")
    else:
        print(f"Erro: {resultado.get('erro')}")


if __name__ == "__main__":
    main()
