# Validação de layout — Proposta PDF (2026-02-13)

## Escopo validado
1. PDF nativo do `gemini_hvac_layout` (Panvel)
2. PDF integrado via bridge `planilha -> gemini_hvac_layout`

## Evidências
- `gemini_hvac_layout/output/grupo_panvel_farmacias/ORC_26.101_GRUPO_PANVEL_FARMACI_INSTALACAO_COMP_R00.pdf`
- `planilha/runtime/demo_outputs/2026-02-13/PROP-2026-0101/client_proposal_integrated.pdf`

## Checklist visual/estrutural
- [x] Número do orçamento e revisão no cabeçalho
- [x] Data e cidade
- [x] Bloco de identificação do cliente (razão social, contato, email, telefone)
- [x] Referência do projeto
- [x] Tabela de serviços/itens
- [x] Investimento total + valor por extenso
- [x] Seções comerciais e exclusões técnicas
- [x] Rodapé institucional e assinaturas
- [x] Documento em PDF multipágina com formatação comercial consistente

## Resultado
**GO (layout aprovado)** para uso operacional.

## Observações
- No PDF integrado, quando dados cadastrais não são enviados no payload, campos aparecem como vazios/N/I (ex.: CNPJ/CPF). Isso não é falha de layout; é ausência de dado de entrada.
- Script `gerar_teste_pdf.sh` foi ajustado para path portável e dependências de runtime foram registradas em `gemini_hvac_layout/requirements.txt`.
