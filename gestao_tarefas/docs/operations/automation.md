# Automação - Sistema de Gestão de Orçamentos

**Versão:** 1.0.0
**Status:** Pronto para uso (NÃO ativo por padrão)
**Última atualização:** 30/01/2026

---

## 📋 Visão Geral

Este diretório contém scripts de automação para processamento contínuo de demandas.

**IMPORTANTE:** Os scripts estão prontos mas **NÃO ATIVOS** por padrão. Você decide quando e como ativar.

### O que pode ser automatizado:

- ✅ **Processar novas demandas** automaticamente
- ✅ **Sincronizar Drive → Asana** periodicamente
- ✅ **Verificar emails novos** de clientes
- ✅ **Gerar relatórios** de atividade
- ✅ **Notificações** de processamentos

---

## 🚀 Quick Start

### 1. Configurar

```bash
# Copiar exemplo de configuração
cp config/automation.config.example.json config/automation.config.json

# Editar conforme necessário
nano config/automation.config.json
```

### 2. Testar Manualmente

```bash
# Dry-run (simular sem executar)
python scripts/ops/scheduler.py job-completo

# Executar de verdade
# (após confirmar que dry-run funciona)
```

### 3. Agendar (Opcional)

Ver seção **Configuração de Cron** abaixo.

---

## 📁 Arquivos

### `scheduler.py` ✅
Script principal de automação.

**Comandos disponíveis:**
```bash
# Processar novas demandas
python scripts/ops/scheduler.py processar-novas

# Sincronizar Drive
python scripts/ops/scheduler.py sync-drive

# Verificar emails (últimos N dias)
python scripts/ops/scheduler.py verificar-emails --dias 2

# Job completo (tudo)
python scripts/ops/scheduler.py job-completo
```

### `config.json.example` ✅
Exemplo de configuração.

**Copiar e editar:**
```bash
cp config/automation.config.example.json config/automation.config.json
```

**Opções principais:**
```json
{
  "dry_run": false,              // Simular ou executar
  "verbose": false,              // Log detalhado
  "processar_automatico": true,  // Processar automaticamente
  "max_demandas_por_vez": 5,     // Limite por execução
  "horarios_processamento": [    // Horários sugeridos
    "09:00",
    "14:00",
    "17:00"
  ]
}
```

### `logs/` (criado automaticamente)
Logs de execução automática.

**Formato:** `scheduler_YYYYMMDD.log`

---

## 🔧 Configuração Detalhada

### config.json

```json
{
  // Modo de teste (recomendado inicialmente)
  "dry_run": true,
  "verbose": true,

  // Processamento
  "processar_automatico": true,
  "max_demandas_por_vez": 5,        // Não sobrecarregar

  // Horários (para referência, não usado pelo script)
  "horarios_processamento": [
    "09:00",  // Manhã - demandas da noite
    "14:00",  // Tarde - demandas da manhã
    "17:00"   // Fim do dia - demandas da tarde
  ],

  // Notificações (futuro)
  "notificar_email": false,
  "email_destino": "orcamentos2@armant.com.br",

  // Verificação de emails
  "dias_verificar_emails": 1,       // Últimas 24h

  // Sincronização
  "sincronizacao": {
    "ativa": true,
    "intervalo_horas": 1            // A cada hora
  },

  // Logging
  "logging": {
    "level": "INFO",
    "manter_logs_dias": 30          // Limpar logs > 30 dias
  }
}
```

---

## ⏰ Configuração de Cron

### Setup Básico

**1. Abrir crontab:**
```bash
crontab -e
```

**2. Adicionar jobs:**
```bash
# Diretório do projeto
PROJECT_DIR=/Users/thiagorosa/dev/tools/armant/gestao-orcamentos

# Job completo 3x por dia (9h, 14h, 17h)
0 9,14,17 * * * cd $PROJECT_DIR && source venv/bin/activate && python scripts/ops/scheduler.py job-completo >> scripts/ops/logs/cron.log 2>&1

# Sincronizar Drive a cada hora
0 * * * * cd $PROJECT_DIR && source venv/bin/activate && python scripts/ops/scheduler.py sync-drive >> scripts/ops/logs/cron_sync.log 2>&1
```

**3. Salvar e sair:**
- Vim: `:wq`
- Nano: `Ctrl+X`, `Y`, `Enter`

**4. Verificar:**
```bash
crontab -l
```

### Exemplos de Agendamento

#### Opção 1: Conservadora (Recomendado para início)
```bash
# Processar 2x por dia (manhã e tarde)
0 9,15 * * * cd $PROJECT_DIR && python scripts/ops/scheduler.py processar-novas

# Sincronizar 1x por dia
0 18 * * * cd $PROJECT_DIR && python scripts/ops/scheduler.py sync-drive
```

**Uso:**
- Baixa carga no sistema
- Processamento manual ainda possível
- Ideal para começar

#### Opção 2: Moderada
```bash
# Processar 3x por dia
0 9,14,17 * * * cd $PROJECT_DIR && python scripts/ops/scheduler.py job-completo
```

**Uso:**
- Processamento regular
- Captura maioria das demandas
- Equilibrado

#### Opção 3: Intensiva
```bash
# Processar a cada 2 horas (horário comercial)
0 8-18/2 * * 1-5 cd $PROJECT_DIR && python scripts/ops/scheduler.py job-completo

# Sincronizar a cada hora
0 * * * * cd $PROJECT_DIR && python scripts/ops/scheduler.py sync-drive
```

**Uso:**
- Alta frequência
- Processamento quasi real-time
- Requer mais recursos

#### Opção 4: Apenas Noturno
```bash
# Processar tudo à noite
0 22 * * * cd $PROJECT_DIR && python scripts/ops/scheduler.py job-completo
```

**Uso:**
- Não interfere no trabalho diário
- Processamento em lote
- Menor carga no sistema

### Sintaxe do Cron

```
* * * * * comando
│ │ │ │ │
│ │ │ │ └── Dia da semana (0-7, 0=Domingo)
│ │ │ └──── Mês (1-12)
│ │ └────── Dia do mês (1-31)
│ └──────── Hora (0-23)
└────────── Minuto (0-59)
```

**Exemplos:**
- `0 9 * * *` - Todo dia às 9h
- `0 9,14,17 * * *` - Todo dia às 9h, 14h e 17h
- `*/30 * * * *` - A cada 30 minutos
- `0 9 * * 1-5` - Dias úteis às 9h
- `0 0 * * 0` - Domingos à meia-noite

---

## 📊 Monitoramento

### Ver Logs

```bash
# Log do dia
tail -f scripts/ops/logs/scheduler_$(date +%Y%m%d).log

# Logs de cron
tail -f scripts/ops/logs/cron.log

# Últimas 50 linhas
tail -50 scripts/ops/logs/scheduler_$(date +%Y%m%d).log

# Buscar erros
grep ERROR scripts/ops/logs/*.log
```

### Verificar Execução

```bash
# Ver últimas execuções do cron
grep CRON /var/log/syslog | tail -20

# macOS
log show --predicate 'eventMessage contains "cron"' --last 1h

# Status do cron
ps aux | grep cron
```

### Limpar Logs Antigos

```bash
# Deletar logs > 30 dias
find scripts/ops/logs -name "*.log" -mtime +30 -delete

# Adicionar ao cron
0 0 * * 0 find $PROJECT_DIR/scripts/ops/logs -name "*.log" -mtime +30 -delete
```

---

## 🧪 Testes

### Antes de Ativar Automação

**1. Testar manualmente:**
```bash
# Dry-run
python scripts/ops/scheduler.py job-completo

# Ver o que seria feito
```

**2. Executar uma vez:**
```bash
# Desativar dry_run no config.json
nano config/automation.config.json
# dry_run: false

# Executar
python scripts/ops/scheduler.py job-completo

# Verificar resultado no Asana
```

**3. Agendar teste:**
```bash
# Agendar para daqui 5 minutos
# Se agora é 14:30, agendar para 14:35

crontab -e
# Adicionar linha temporária:
35 14 * * * cd $PROJECT_DIR && python scripts/ops/scheduler.py job-completo

# Aguardar e verificar log
```

**4. Se funcionou, configurar horários definitivos**

---

## ⚠️ Avisos Importantes

### Antes de Ativar

- [ ] Testar manualmente com `--dry-run`
- [ ] Executar manualmente sem dry-run (1x)
- [ ] Verificar se credenciais estão configuradas
- [ ] Confirmar que não há duplicatas no Asana
- [ ] Ter backup do sistema

### Durante Uso

- ⚠️ **Monitorar logs** nos primeiros dias
- ⚠️ **Verificar Asana** regularmente
- ⚠️ **Ajustar frequência** conforme necessário
- ⚠️ **Pausar se problemas** (comentar linha do cron)

### Desativar Temporariamente

```bash
# Editar crontab
crontab -e

# Comentar linha (adicionar # no início)
# 0 9,14,17 * * * cd $PROJECT_DIR && python scripts/ops/scheduler.py job-completo

# Salvar

# Ou remover completamente
crontab -r  # Remove TODOS os cron jobs
```

---

## 🔧 Troubleshooting

### Cron não executa

**Problema:** Jobs agendados não rodam

**Diagnóstico:**
```bash
# Ver logs do sistema
tail -f /var/log/syslog | grep CRON  # Linux
log stream --level debug | grep cron  # macOS

# Verificar sintaxe do cron
crontab -l
```

**Soluções:**
1. Usar caminhos absolutos
2. Ativar ambiente virtual no comando
3. Redirecionar output: `>> log.txt 2>&1`
4. Testar comando manualmente primeiro

### Ambiente virtual não ativa

**Problema:** `ModuleNotFoundError` nos logs

**Solução:**
```bash
# No cron, usar caminho completo
0 9 * * * /full/path/to/venv/bin/python /full/path/to/scripts/ops/scheduler.py job-completo

# Ou ativar venv explicitamente
0 9 * * * cd $PROJECT_DIR && source venv/bin/activate && python scripts/ops/scheduler.py job-completo
```

### Credenciais não encontradas

**Problema:** Erros de autenticação nos logs

**Solução:**
```bash
# Garantir que .env está no diretório correto
ls -la .env

# Testar manualmente com mesmo comando do cron
cd /path/to/project && source venv/bin/activate && python scripts/ops/scheduler.py job-completo
```

### Muitas demandas processadas

**Problema:** Sistema processa demandas já processadas

**Solução:**
1. Verificar `ids_mapping.json` está atualizado
2. Reduzir `max_demandas_por_vez` no config
3. Usar `--dry-run` para testar

### Logs muito grandes

**Problema:** Logs ocupando muito espaço

**Solução:**
```bash
# Configurar rotação de logs
# Adicionar ao cron:
0 0 * * 0 find $PROJECT_DIR/scripts/ops/logs -name "*.log" -mtime +7 -delete

# Ou usar logrotate (Linux)
```

---

## 📚 Recursos

### Ferramentas Úteis

- **Cron Generator:** [crontab.guru](https://crontab.guru/)
- **Teste de Cron:** `crontab -l` e testar comando manualmente
- **Logs:** `tail -f scripts/ops/logs/scheduler_*.log`

### Documentação

- **Scheduler:** Ver código em `scripts/ops/scheduler.py`
- **CLI:** Ver `GUIA_USUARIO.md`
- **Troubleshooting:** Ver `TROUBLESHOOTING.md`

---

## 🔮 Futuras Melhorias

Funcionalidades planejadas mas não implementadas:

- [ ] Watch folder (monitorar pasta Drive em tempo real)
- [ ] Notificações por email
- [ ] Dashboard web de monitoramento
- [ ] Integração com Slack/Teams
- [ ] Machine learning para priorização
- [ ] API REST para controle remoto

---

## 📝 Changelog

**1.0.0 (30/01/2026)**
- Versão inicial do scheduler
- Jobs: processar-novas, sync-drive, verificar-emails, job-completo
- Sistema de configuração JSON
- Logging estruturado
- Relatórios automáticos

---

## 📞 Suporte

**Problemas com automação:**
1. Verificar logs: `scripts/ops/logs/`
2. Testar manualmente
3. Consultar troubleshooting
4. Reportar bug com logs anexados

**Desativar urgentemente:**
```bash
crontab -e
# Comentar linhas com #
# Ou: crontab -r (remove tudo)
```

---

**Última atualização:** 30/01/2026
**Versão do sistema:** 1.0.0
**Status:** Pronto para uso (não ativo por padrão)
