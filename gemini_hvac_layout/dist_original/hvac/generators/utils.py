#!/usr/bin/env python3
"""
Utilitarios para geracao de documentos HVAC
"""

import json
from datetime import date, datetime
from pathlib import Path
from typing import Dict, Any, Optional, Tuple

# Diretorio base do projeto
BASE_DIR = Path(__file__).parent.parent.parent


def carregar_configs() -> Dict[str, Any]:
    """
    Carrega todas as configuracoes do sistema

    Returns:
        Dicionario com todas as configs
    """
    config_dir = BASE_DIR / "config"

    configs = {}

    # Empresa
    empresa_path = config_dir / "empresa.json"
    if empresa_path.exists():
        with open(empresa_path, "r", encoding="utf-8") as f:
            configs["empresa"] = json.load(f)

    # Usuario
    usuario_path = config_dir / "usuario.json"
    if usuario_path.exists():
        with open(usuario_path, "r", encoding="utf-8") as f:
            configs["usuario"] = json.load(f)

    # Condicoes comerciais
    condicoes_path = config_dir / "condicoes_comerciais.json"
    if condicoes_path.exists():
        with open(condicoes_path, "r", encoding="utf-8") as f:
            configs["condicoes"] = json.load(f)

    # Contador
    contador_path = config_dir / "contador.json"
    if contador_path.exists():
        with open(contador_path, "r", encoding="utf-8") as f:
            configs["contador"] = json.load(f)

    # Exclusoes
    exclusoes_path = config_dir / "exclusoes.json"
    if exclusoes_path.exists():
        with open(exclusoes_path, "r", encoding="utf-8") as f:
            configs["exclusoes"] = json.load(f)

    return configs


def salvar_contador(contador: Dict[str, Any]) -> None:
    """Salva o contador atualizado"""
    config_dir = BASE_DIR / "config"
    contador_path = config_dir / "contador.json"

    with open(contador_path, "w", encoding="utf-8") as f:
        json.dump(contador, f, ensure_ascii=False, indent=2)


def proximo_numero_orcamento(configs: Optional[Dict] = None) -> Tuple[str, int]:
    """
    Gera o proximo numero de orcamento

    Args:
        configs: Configuracoes (carrega se nao fornecido)

    Returns:
        Tupla (numero_formatado, sequencial)
        Ex: ("2025/868-R00", 868)
    """
    if configs is None:
        configs = carregar_configs()

    contador = configs.get("contador", {})
    ano_atual = date.today().year

    # Verifica virada de ano
    ano_contador = contador.get("ano_corrente", ano_atual)

    if ano_atual != ano_contador:
        # Virou o ano - salva historico e reseta
        contador["historico"] = contador.get("historico", {})
        contador["historico"][str(ano_contador)] = contador.get("ultimo_sequencial", 0)
        contador["ano_corrente"] = ano_atual
        contador["ultimo_sequencial"] = 0

    # Incrementa sequencial
    novo_seq = contador.get("ultimo_sequencial", 0) + 1
    contador["ultimo_sequencial"] = novo_seq
    contador["ano_corrente"] = ano_atual

    # Salva contador atualizado
    salvar_contador(contador)

    # Formata numero
    numero = f"{ano_atual}/{novo_seq:03d}-R00"

    return numero, novo_seq


def detectar_revisao(cliente: str, output_dir: Path) -> Tuple[str, int]:
    """
    Detecta se existe orcamento anterior para o cliente e gera revisao

    Args:
        cliente: Nome do cliente
        output_dir: Diretorio de output

    Returns:
        Tupla (sufixo_revisao, numero_revisao)
        Ex: ("R01", 1)
    """
    if not output_dir.exists():
        return "R00", 0

    # Busca arquivos existentes do cliente
    cliente_slug = cliente.lower().replace(" ", "_")[:20]
    arquivos = list(output_dir.glob(f"*{cliente_slug}*_R*.pdf"))

    if not arquivos:
        return "R00", 0

    # Encontra maior revisao
    max_rev = 0
    for arq in arquivos:
        nome = arq.stem
        if "_R" in nome:
            try:
                rev_str = nome.split("_R")[-1].split("_")[0]
                rev = int(rev_str)
                if rev > max_rev:
                    max_rev = rev
            except (ValueError, IndexError):
                pass

    nova_rev = max_rev + 1
    return f"R{nova_rev:02d}", nova_rev


def formatar_moeda(valor: float) -> str:
    """
    Formata valor como moeda brasileira

    Args:
        valor: Valor numerico

    Returns:
        String formatada (ex: "11.097,90")
    """
    return f"{valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


def formatar_numero(valor: float) -> str:
    """
    Formata numero com decimais brasileiros

    Args:
        valor: Valor numerico

    Returns:
        String formatada (ex: "1,00" ou "15")
    """
    if valor == int(valor):
        return str(int(valor))
    return f"{valor:.2f}".replace(".", ",")


def numero_por_extenso(numero: int) -> str:
    """
    Converte numero para extenso

    Args:
        numero: Numero inteiro (0-999)

    Returns:
        Numero por extenso
    """
    unidades = [
        "", "um", "dois", "tres", "quatro", "cinco",
        "seis", "sete", "oito", "nove", "dez",
        "onze", "doze", "treze", "quatorze", "quinze",
        "dezesseis", "dezessete", "dezoito", "dezenove"
    ]

    dezenas = [
        "", "", "vinte", "trinta", "quarenta", "cinquenta",
        "sessenta", "setenta", "oitenta", "noventa"
    ]

    centenas = [
        "", "cento", "duzentos", "trezentos", "quatrocentos", "quinhentos",
        "seiscentos", "setecentos", "oitocentos", "novecentos"
    ]

    if numero == 0:
        return "zero"
    if numero == 100:
        return "cem"

    resultado = []

    # Centenas
    if numero >= 100:
        resultado.append(centenas[numero // 100])
        numero = numero % 100

    # Dezenas e unidades
    if numero > 0:
        if numero < 20:
            resultado.append(unidades[numero])
        else:
            resultado.append(dezenas[numero // 10])
            if numero % 10 > 0:
                resultado.append(unidades[numero % 10])

    return " e ".join([r for r in resultado if r])


def valor_por_extenso(valor: float) -> str:
    """
    Converte valor monetario para extenso

    Args:
        valor: Valor em reais

    Returns:
        Valor por extenso
    """
    reais = int(valor)
    centavos = round((valor - reais) * 100)

    partes = []

    # Milhoes
    if reais >= 1000000:
        milhoes = reais // 1000000
        if milhoes == 1:
            partes.append("um milhao")
        else:
            partes.append(f"{numero_por_extenso(milhoes)} milhoes")
        reais = reais % 1000000

    # Milhares
    if reais >= 1000:
        milhares = reais // 1000
        partes.append(f"{numero_por_extenso(milhares)} mil")
        reais = reais % 1000

    # Centenas/dezenas/unidades
    if reais > 0:
        partes.append(numero_por_extenso(reais))

    # Monta texto dos reais
    if partes:
        texto_reais = " e ".join(partes)
        if int(valor) == 1:
            texto_reais += " real"
        else:
            texto_reais += " reais"
    else:
        texto_reais = "zero reais"

    # Centavos
    if centavos > 0:
        texto_centavos = numero_por_extenso(centavos)
        if centavos == 1:
            texto_centavos += " centavo"
        else:
            texto_centavos += " centavos"
        return f"{texto_reais} e {texto_centavos}"

    return texto_reais


def data_por_extenso(data: date = None) -> str:
    """
    Formata data por extenso

    Args:
        data: Data (usa hoje se nao informado)

    Returns:
        Data formatada (ex: "18 de dezembro de 2025")
    """
    if data is None:
        data = date.today()

    meses = [
        "", "janeiro", "fevereiro", "março", "abril", "maio", "junho",
        "julho", "agosto", "setembro", "outubro", "novembro", "dezembro"
    ]

    return f"{data.day} de {meses[data.month]} de {data.year}"


def obter_exclusoes(tipo_servico: str, configs: Optional[Dict] = None) -> list:
    """
    Obtem lista de exclusoes para o tipo de servico

    Args:
        tipo_servico: Tipo do servico (instalacao, manutencao-preventiva, etc)
        configs: Configuracoes

    Returns:
        Lista de exclusoes
    """
    if configs is None:
        configs = carregar_configs()

    exclusoes = configs.get("exclusoes", {})

    # Tenta tipo exato
    if tipo_servico in exclusoes:
        return exclusoes[tipo_servico]

    # Tenta tipo generico (instalacao-completa -> instalacao)
    tipo_generico = tipo_servico.split("-")[0]
    if tipo_generico in exclusoes:
        return exclusoes[tipo_generico]

    # Fallback para instalacao
    return exclusoes.get("instalacao", [])


def obter_condicoes(tipo_cliente: str, configs: Optional[Dict] = None) -> Dict[str, Any]:
    """
    Obtem condicoes comerciais para o tipo de cliente

    Args:
        tipo_cliente: Tipo do cliente (PRIVADO-PJ, PRIVADO-PF, GOVERNO)
        configs: Configuracoes

    Returns:
        Dicionario com condicoes
    """
    if configs is None:
        configs = carregar_configs()

    condicoes_config = configs.get("condicoes", {})
    default = condicoes_config.get("default", {})
    por_tipo = condicoes_config.get("por_tipo_cliente", {}).get(tipo_cliente, {})

    # Mescla default com especifico do tipo
    resultado = {**default, **por_tipo}

    # Adiciona extenso da validade
    validade = resultado.get("validade_dias", 10)
    resultado["validade_extenso"] = numero_por_extenso(validade)

    return resultado


def criar_pasta_cliente(cliente: str) -> Path:
    """
    Cria pasta de output para o cliente

    Args:
        cliente: Nome do cliente

    Returns:
        Path da pasta criada
    """
    output_dir = BASE_DIR / "output"

    # Cria slug do cliente
    import re
    slug = re.sub(r'[^\w\s-]', '', cliente.lower())
    slug = re.sub(r'[-\s]+', '_', slug)[:30]

    cliente_dir = output_dir / slug
    cliente_dir.mkdir(parents=True, exist_ok=True)

    return cliente_dir


def gerar_nome_arquivo(
    numero_orcamento: str,
    cliente: str,
    tipo_servico: str,
    revisao: str = "R00",
    sufixo: str = ""
) -> str:
    """
    Gera nome padronizado para arquivo

    Args:
        numero_orcamento: Numero do orcamento (ex: "2025/868")
        cliente: Nome do cliente
        tipo_servico: Tipo do servico
        revisao: Revisao (ex: "R00")
        sufixo: Sufixo adicional (ex: "_interno", "_RASCUNHO")

    Returns:
        Nome do arquivo sem extensao
    """
    import re

    # Extrai ano e numero
    partes = numero_orcamento.replace("-", "/").split("/")
    ano = partes[0][-2:]  # Ultimos 2 digitos do ano
    num = partes[1].split("-")[0] if len(partes) > 1 else "000"

    # Slug do cliente
    slug_cliente = re.sub(r'[^\w\s-]', '', cliente.upper())
    slug_cliente = re.sub(r'[-\s]+', '_', slug_cliente)[:20]

    # Slug do servico
    slug_servico = tipo_servico.upper().replace("-", "_")[:15]

    return f"ORC_{ano}.{num}_{slug_cliente}_{slug_servico}_{revisao}{sufixo}"
