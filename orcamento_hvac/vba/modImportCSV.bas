Attribute VB_Name = "modImportCSV"
Option Explicit

' =============================================================================
' MODULO: modImportCSV
' Importacao de dados CSV para atualizacao de catalogos
' VERSAO 2.0 - Com validade por item
'
' Arquivos CSV esperados na pasta dados_csv/:
'   - materiais_{YYYY-MM-DD}.csv
'   - mao_de_obra_{YYYY-MM-DD}.csv
'   - ferramentas_{YYYY-MM-DD}.csv
'   - equipamentos_{YYYY-MM-DD}.csv
'
' O sistema importa automaticamente o arquivo mais recente de cada tipo.
' Cada item possui colunas ATUALIZADO_EM e VALIDADE_DIAS para controle individual.
'
' Especificacoes CSV:
'   - Encoding: UTF-8 com BOM
'   - Delimitador: ; (ponto-e-virgula)
'   - Quebra de linha: CRLF
' =============================================================================

' Configuracoes
Private Const CSV_DELIMITER As String = ";"
Private Const CONFIG_SHEET As String = "NEGOCIO"
Private Const PATH_CELL As String = "A57"
Private Const TIMESTAMP_CELL As String = "B58"
Private Const STATUS_CELL As String = "B59"
Private Const DEFAULT_CSV_PATH As String = ".\dados_csv\"

' Cores para formatacao condicional
Private Const COLOR_EXPIRED As Long = 13408767    ' Vermelho claro RGB(255, 200, 200)
Private Const COLOR_EXPIRING As Long = 13434828   ' Amarelo claro RGB(255, 255, 200)

' Estrutura de configuracao de catalogo
Private Type CatalogConfig
    SheetName As String
    FilePrefix As String
    NumDataCols As Integer
    SelectionCol As Integer
    SelectionFormula As String
    NamedRange As String
    HasCustoHoraCol As Boolean
    CustoHoraCol As Integer
    AtualizadoEmCol As Integer
    ValidadeDiasCol As Integer
End Type

' =============================================================================
' FUNCOES PUBLICAS
' =============================================================================

' -----------------------------------------------------------------------------
' ImportarTodosCatalogos - Importa todos os 4 catalogos de uma vez
' -----------------------------------------------------------------------------
Public Sub ImportarTodosCatalogos()
    Dim catalogos As Variant
    Dim i As Long
    Dim successCount As Long
    Dim errorLog As String
    Dim startTime As Double

    catalogos = Array("MATERIAIS", "MAO_DE_OBRA", "FERRAMENTAS", "EQUIPAMENTOS")

    startTime = Timer
    Application.ScreenUpdating = False
    Application.Calculation = xlCalculationManual

    successCount = 0
    errorLog = ""

    For i = 0 To UBound(catalogos)
        Application.StatusBar = "Importando " & catalogos(i) & "..."

        On Error Resume Next
        Call ImportarCatalogoInterno(CStr(catalogos(i)), False)
        If Err.Number = 0 Then
            successCount = successCount + 1
        Else
            errorLog = errorLog & catalogos(i) & ": " & Err.Description & vbCrLf
            Err.Clear
        End If
        On Error GoTo 0
    Next i

    Application.StatusBar = False
    Application.Calculation = xlCalculationAutomatic
    Application.ScreenUpdating = True

    ' Atualizar timestamp
    Call AtualizarTimestamp

    ' Verificar validade apos importacao
    Dim validadeMsg As String
    validadeMsg = VerificarValidadeInterna(False)

    ' Mostrar resultado
    Dim tempoTotal As String
    tempoTotal = Format(Timer - startTime, "0.0") & "s"

    If errorLog = "" Then
        MsgBox "Importacao concluida com sucesso!" & vbCrLf & vbCrLf & _
               successCount & " catalogos atualizados em " & tempoTotal & "." & _
               IIf(validadeMsg <> "", vbCrLf & vbCrLf & validadeMsg, ""), _
               vbInformation, "Importacao Concluida"
    Else
        MsgBox "Importacao concluida com erros:" & vbCrLf & vbCrLf & errorLog, _
               vbExclamation, "Erros na Importacao"
    End If
End Sub

' -----------------------------------------------------------------------------
' ImportarCatalogo - Importa um catalogo especifico
' -----------------------------------------------------------------------------
Public Sub ImportarCatalogo(ByVal catalogName As String)
    Call ImportarCatalogoInterno(catalogName, True)
End Sub

' -----------------------------------------------------------------------------
' VerificarValidade - Verifica se algum item esta vencido (por item)
' -----------------------------------------------------------------------------
Public Sub VerificarValidade()
    Dim msg As String
    msg = VerificarValidadeInterna(True)

    If msg = "" Then
        MsgBox "Todos os itens estao dentro da validade.", _
               vbInformation, "Validade OK"
    End If
End Sub

' -----------------------------------------------------------------------------
' AbrirPastaCSV - Abre a pasta de CSVs no Windows Explorer
' -----------------------------------------------------------------------------
Public Sub AbrirPastaCSV()
    Dim csvPath As String
    Dim fullPath As String

    csvPath = GetCSVPath()
    fullPath = BuildFullPath(csvPath)

    If Dir(fullPath, vbDirectory) = "" Then
        MsgBox "Pasta nao encontrada:" & vbCrLf & fullPath & vbCrLf & vbCrLf & _
               "Verifique o caminho configurado na aba NEGOCIO.", _
               vbExclamation, "Pasta Nao Encontrada"
        Exit Sub
    End If

    Shell "explorer.exe """ & fullPath & """", vbNormalFocus
End Sub

' =============================================================================
' FUNCOES INTERNAS
' =============================================================================

' -----------------------------------------------------------------------------
' ImportarCatalogoInterno - Logica principal de importacao
' -----------------------------------------------------------------------------
Private Sub ImportarCatalogoInterno(ByVal catalogName As String, ByVal showMessage As Boolean)
    Dim config As CatalogConfig
    Dim ws As Worksheet
    Dim filePath As String
    Dim csvData As Variant
    Dim lastRow As Long
    Dim errors As String

    ' 1. Obter configuracao do catalogo
    config = GetCatalogConfig(catalogName)
    If config.SheetName = "" Then
        If showMessage Then
            MsgBox "Catalogo desconhecido: " & catalogName, vbExclamation
        End If
        Err.Raise 1001, , "Catalogo desconhecido: " & catalogName
        Exit Sub
    End If

    ' 2. Buscar arquivo mais recente
    filePath = EncontrarArquivoMaisRecente(GetCSVPath(), config.FilePrefix)
    If filePath = "" Then
        If showMessage Then
            MsgBox "Nenhum arquivo encontrado para: " & config.FilePrefix & "_*.csv" & vbCrLf & _
                   "Pasta: " & GetCSVPath(), vbExclamation
        End If
        Err.Raise 1002, , "Arquivo nao encontrado: " & config.FilePrefix
        Exit Sub
    End If

    ' 3. Ler dados do CSV
    csvData = ReadCSVFile(filePath)
    If IsEmpty(csvData) Then
        If showMessage Then
            MsgBox "Arquivo CSV vazio ou invalido:" & vbCrLf & filePath, vbExclamation
        End If
        Err.Raise 1003, , "CSV vazio: " & filePath
        Exit Sub
    End If

    ' 4. Validar dados
    errors = ValidateCSVData(csvData, config)
    If errors <> "" Then
        If showMessage Then
            MsgBox "Erros de validacao em " & config.FilePrefix & ":" & vbCrLf & vbCrLf & _
                   Left(errors, 500), vbExclamation, "Erros de Validacao"
        End If
        ' Continua mesmo com erros de validacao (avisos)
    End If

    ' 5. Obter worksheet
    On Error Resume Next
    Set ws = ThisWorkbook.Sheets(config.SheetName)
    On Error GoTo 0

    If ws Is Nothing Then
        If showMessage Then
            MsgBox "Aba nao encontrada: " & config.SheetName, vbCritical
        End If
        Err.Raise 1004, , "Aba nao encontrada: " & config.SheetName
        Exit Sub
    End If

    ' 6. Limpar dados existentes (manter header)
    Call ClearCatalogData(ws, config)

    ' 7. Escrever dados e formulas
    lastRow = WriteDataToSheet(ws, csvData, config)

    ' 8. Aplicar formatacao condicional por validade
    Call AplicarFormatacaoValidade(ws, config, lastRow)

    ' 9. Atualizar intervalo nomeado
    Call AtualizarIntervaloNomeadoImport(config.NamedRange, config.SheetName, _
                                          config.SelectionCol, lastRow)

    ' 10. Mensagem de sucesso
    If showMessage Then
        MsgBox "Catalogo " & catalogName & " importado com sucesso!" & vbCrLf & _
               UBound(csvData, 1) & " itens carregados de:" & vbCrLf & _
               Dir(filePath), _
               vbInformation, "Importacao Concluida"
    End If
End Sub

' -----------------------------------------------------------------------------
' GetCatalogConfig - Retorna configuracao do catalogo (versao 2.0 com validade)
' -----------------------------------------------------------------------------
Private Function GetCatalogConfig(catalogName As String) As CatalogConfig
    Dim cfg As CatalogConfig

    Select Case UCase(catalogName)
        Case "MATERIAIS"
            ' Colunas: A-Codigo, B-Categoria, C-Descricao, D-Unidade, E-Preco,
            '          F-AtualizadoEm, G-ValidadeDias, H-Selecao
            cfg.SheetName = "MATERIAIS"
            cfg.FilePrefix = "materiais"
            cfg.NumDataCols = 7       ' A-G: dados do CSV
            cfg.SelectionCol = 8      ' H: Selecao
            cfg.SelectionFormula = "=A{ROW}&"" - ""&C{ROW}"
            cfg.NamedRange = "LISTA_MAT"
            cfg.HasCustoHoraCol = False
            cfg.AtualizadoEmCol = 6   ' F
            cfg.ValidadeDiasCol = 7   ' G

        Case "MAO_DE_OBRA"
            ' Colunas: A-Codigo, B-Categoria, C-Descricao, D-Unidade, E-Custo,
            '          F-AtualizadoEm, G-ValidadeDias, H-Selecao
            cfg.SheetName = "MAO_DE_OBRA"
            cfg.FilePrefix = "mao_de_obra"
            cfg.NumDataCols = 7
            cfg.SelectionCol = 8
            cfg.SelectionFormula = "=A{ROW}&"" - ""&C{ROW}"
            cfg.NamedRange = "LISTA_MO"
            cfg.HasCustoHoraCol = False
            cfg.AtualizadoEmCol = 6
            cfg.ValidadeDiasCol = 7

        Case "FERRAMENTAS"
            ' Colunas: A-Codigo, B-Categoria, C-Descricao, D-ValorAquisicao, E-VidaUtil,
            '          F-CustoHora (formula), G-AtualizadoEm, H-ValidadeDias, I-Selecao
            cfg.SheetName = "FERRAMENTAS"
            cfg.FilePrefix = "ferramentas"
            cfg.NumDataCols = 7       ' A-E do CSV + G-H (validade) = 7 colunas de dados
            cfg.SelectionCol = 9      ' I: Selecao
            cfg.SelectionFormula = "=A{ROW}&"" - ""&C{ROW}"
            cfg.NamedRange = "LISTA_FER"
            cfg.HasCustoHoraCol = True
            cfg.CustoHoraCol = 6      ' F: CustoHora = D/E
            cfg.AtualizadoEmCol = 7   ' G
            cfg.ValidadeDiasCol = 8   ' H

        Case "EQUIPAMENTOS"
            ' Colunas: A-Codigo, B-Categoria, C-Descricao, D-Capacidade, E-Unidade,
            '          F-Preco, G-AtualizadoEm, H-ValidadeDias, I-Selecao
            cfg.SheetName = "EQUIPAMENTOS"
            cfg.FilePrefix = "equipamentos"
            cfg.NumDataCols = 8       ' A-H: dados do CSV
            cfg.SelectionCol = 9      ' I: Selecao
            cfg.SelectionFormula = "=A{ROW}&"" - ""&C{ROW}"
            cfg.NamedRange = "LISTA_EQP"
            cfg.HasCustoHoraCol = False
            cfg.AtualizadoEmCol = 7   ' G
            cfg.ValidadeDiasCol = 8   ' H

        Case Else
            cfg.SheetName = ""
    End Select

    GetCatalogConfig = cfg
End Function

' -----------------------------------------------------------------------------
' EncontrarArquivoMaisRecente - Busca arquivo mais recente por prefixo
' Padrao: {prefixo}_{YYYY-MM-DD}.csv
' -----------------------------------------------------------------------------
Private Function EncontrarArquivoMaisRecente(csvPath As String, prefix As String) As String
    Dim fullPath As String
    Dim fileName As String
    Dim bestFile As String
    Dim bestDate As String
    Dim fileDate As String
    Dim pattern As String

    fullPath = BuildFullPath(csvPath)
    pattern = prefix & "_*.csv"

    bestFile = ""
    bestDate = ""

    fileName = Dir(fullPath & pattern)
    Do While fileName <> ""
        ' Extrair data do nome do arquivo (formato: prefixo_YYYY-MM-DD.csv)
        fileDate = ExtractDateFromFileName(fileName, prefix)

        If fileDate <> "" Then
            ' Comparar strings de data (YYYY-MM-DD ordena corretamente)
            If fileDate > bestDate Then
                bestDate = fileDate
                bestFile = fileName
            End If
        End If

        fileName = Dir()
    Loop

    If bestFile <> "" Then
        EncontrarArquivoMaisRecente = fullPath & bestFile
    Else
        EncontrarArquivoMaisRecente = ""
    End If
End Function

' -----------------------------------------------------------------------------
' ExtractDateFromFileName - Extrai data do nome do arquivo
' -----------------------------------------------------------------------------
Private Function ExtractDateFromFileName(fileName As String, prefix As String) As String
    Dim datePart As String
    Dim startPos As Long
    Dim endPos As Long

    ' Formato esperado: prefixo_YYYY-MM-DD.csv
    startPos = Len(prefix) + 2  ' Apos prefixo e underscore
    endPos = InStr(fileName, ".csv")

    If endPos > startPos Then
        datePart = Mid(fileName, startPos, endPos - startPos)

        ' Validar formato YYYY-MM-DD (10 caracteres)
        If Len(datePart) = 10 And Mid(datePart, 5, 1) = "-" And Mid(datePart, 8, 1) = "-" Then
            ExtractDateFromFileName = datePart
        Else
            ExtractDateFromFileName = ""
        End If
    Else
        ExtractDateFromFileName = ""
    End If
End Function

' -----------------------------------------------------------------------------
' GetCSVPath - Obtem caminho dos CSVs da configuracao
' -----------------------------------------------------------------------------
Private Function GetCSVPath() As String
    Dim ws As Worksheet
    Dim path As String

    On Error Resume Next
    Set ws = ThisWorkbook.Sheets(CONFIG_SHEET)
    On Error GoTo 0

    If ws Is Nothing Then
        GetCSVPath = DEFAULT_CSV_PATH
        Exit Function
    End If

    path = Trim(CStr(ws.Range(PATH_CELL).Value))
    If path = "" Then
        path = DEFAULT_CSV_PATH
    End If

    ' Garantir que termina com \
    If Right(path, 1) <> "\" Then
        path = path & "\"
    End If

    GetCSVPath = path
End Function

' -----------------------------------------------------------------------------
' BuildFullPath - Converte caminho relativo para absoluto
' -----------------------------------------------------------------------------
Private Function BuildFullPath(relativePath As String) As String
    Dim basePath As String

    ' Se ja e absoluto, retorna como esta
    If Mid(relativePath, 2, 1) = ":" Or Left(relativePath, 2) = "\\" Then
        BuildFullPath = relativePath
        Exit Function
    End If

    ' Obtem pasta do workbook
    basePath = ThisWorkbook.path
    If basePath = "" Then
        basePath = CurDir
    End If

    ' Remove .\ do inicio se presente
    If Left(relativePath, 2) = ".\" Then
        relativePath = Mid(relativePath, 3)
    End If

    BuildFullPath = basePath & "\" & relativePath
End Function

' -----------------------------------------------------------------------------
' FileExists - Verifica se arquivo existe
' -----------------------------------------------------------------------------
Private Function FileExists(path As String) As Boolean
    On Error Resume Next
    FileExists = (Dir(path) <> "")
    On Error GoTo 0
End Function

' -----------------------------------------------------------------------------
' ReadCSVFile - Le arquivo CSV com encoding UTF-8
' -----------------------------------------------------------------------------
Private Function ReadCSVFile(filePath As String) As Variant
    Dim stream As Object
    Dim content As String
    Dim lines() As String
    Dim fields() As String
    Dim data() As Variant
    Dim i As Long, j As Long
    Dim numRows As Long, numCols As Long

    ' Usar ADODB.Stream para ler UTF-8
    Set stream = CreateObject("ADODB.Stream")
    stream.Type = 2  ' adTypeText
    stream.Charset = "utf-8"
    stream.Open
    stream.LoadFromFile filePath
    content = stream.ReadText(-1)  ' adReadAll
    stream.Close
    Set stream = Nothing

    ' Remover BOM se presente
    If Left(content, 1) = Chr(65279) Then
        content = Mid(content, 2)
    End If

    ' Dividir em linhas
    lines = Split(content, vbCrLf)

    ' Remover linha vazia no final se existir
    If lines(UBound(lines)) = "" Then
        ReDim Preserve lines(UBound(lines) - 1)
    End If

    ' Pular header (linha 0), contar linhas de dados
    numRows = UBound(lines)  ' Linhas 1 a n
    If numRows < 1 Then
        ReadCSVFile = Empty
        Exit Function
    End If

    ' Obter numero de colunas do header
    fields = Split(lines(0), CSV_DELIMITER)
    numCols = UBound(fields) + 1

    ' Alocar array (1-based para compatibilidade com Excel)
    ReDim data(1 To numRows, 1 To numCols)

    ' Parsear linhas de dados (pular header no indice 0)
    For i = 1 To numRows
        fields = ParseCSVLine(lines(i))
        For j = 0 To UBound(fields)
            If j < numCols Then
                data(i, j + 1) = CleanCSVField(fields(j))
            End If
        Next j
    Next i

    ReadCSVFile = data
End Function

' -----------------------------------------------------------------------------
' ParseCSVLine - Parseia linha CSV respeitando aspas
' -----------------------------------------------------------------------------
Private Function ParseCSVLine(line As String) As String()
    Dim result() As String
    Dim inQuotes As Boolean
    Dim currentField As String
    Dim fieldCount As Long
    Dim i As Long
    Dim c As String

    ReDim result(0 To 0)
    inQuotes = False
    currentField = ""
    fieldCount = 0

    For i = 1 To Len(line)
        c = Mid(line, i, 1)

        If c = """" Then
            If inQuotes And Mid(line, i + 1, 1) = """" Then
                ' Aspas escapadas
                currentField = currentField & """"
                i = i + 1
            Else
                inQuotes = Not inQuotes
            End If
        ElseIf c = CSV_DELIMITER And Not inQuotes Then
            ' Fim do campo
            ReDim Preserve result(0 To fieldCount)
            result(fieldCount) = currentField
            currentField = ""
            fieldCount = fieldCount + 1
        Else
            currentField = currentField & c
        End If
    Next i

    ' Ultimo campo
    ReDim Preserve result(0 To fieldCount)
    result(fieldCount) = currentField

    ParseCSVLine = result
End Function

' -----------------------------------------------------------------------------
' CleanCSVField - Limpa campo CSV
' -----------------------------------------------------------------------------
Private Function CleanCSVField(field As String) As Variant
    Dim cleaned As String
    Dim numValue As Double

    cleaned = Trim(field)

    ' Remover aspas ao redor
    If Left(cleaned, 1) = """" And Right(cleaned, 1) = """" Then
        cleaned = Mid(cleaned, 2, Len(cleaned) - 2)
    End If

    ' Tentar converter para numero se possivel
    If IsNumeric(cleaned) Then
        ' Tratar virgula como decimal (locale brasileiro)
        cleaned = Replace(cleaned, ",", ".")
        On Error Resume Next
        numValue = CDbl(cleaned)
        If Err.Number = 0 Then
            CleanCSVField = numValue
            Exit Function
        End If
        On Error GoTo 0
    End If

    CleanCSVField = cleaned
End Function

' -----------------------------------------------------------------------------
' ValidateCSVData - Valida dados do CSV
' -----------------------------------------------------------------------------
Private Function ValidateCSVData(data As Variant, config As CatalogConfig) As String
    Dim errors As String
    Dim i As Long
    Dim codigo As String
    Dim codigosUsados As Object

    Set codigosUsados = CreateObject("Scripting.Dictionary")
    errors = ""

    For i = 1 To UBound(data, 1)
        codigo = Trim(CStr(data(i, 1)))

        ' Verificar codigo obrigatorio
        If codigo = "" Then
            errors = errors & "Linha " & (i + 1) & ": Codigo vazio" & vbCrLf
        Else
            ' Verificar duplicatas
            If codigosUsados.Exists(codigo) Then
                errors = errors & "Linha " & (i + 1) & ": Codigo duplicado '" & codigo & "'" & vbCrLf
            Else
                codigosUsados.Add codigo, i
            End If

            ' Verificar prefixo (apenas aviso)
            If Not ValidateCodePrefix(codigo, config.SheetName) Then
                ' Apenas aviso, nao bloqueia
            End If
        End If
    Next i

    ValidateCSVData = errors
End Function

' -----------------------------------------------------------------------------
' ValidateCodePrefix - Valida prefixo do codigo
' -----------------------------------------------------------------------------
Private Function ValidateCodePrefix(codigo As String, sheetName As String) As Boolean
    Select Case sheetName
        Case "MAO_DE_OBRA"
            ValidateCodePrefix = (Left(codigo, 3) = "MO_")
        Case "FERRAMENTAS"
            ValidateCodePrefix = (Left(codigo, 4) = "FER_")
        Case "EQUIPAMENTOS"
            ValidateCodePrefix = (Left(codigo, 4) = "EQP_")
        Case Else
            ValidateCodePrefix = True  ' MATERIAIS nao tem prefixo fixo
    End Select
End Function

' -----------------------------------------------------------------------------
' ClearCatalogData - Limpa dados existentes mantendo header
' -----------------------------------------------------------------------------
Private Sub ClearCatalogData(ws As Worksheet, config As CatalogConfig)
    Dim lastRow As Long
    Dim lastCol As Integer

    lastRow = ws.Cells(ws.Rows.count, 1).End(xlUp).row
    If lastRow < 2 Then Exit Sub

    lastCol = config.SelectionCol

    ' Limpar area de dados (linha 2 ate o fim)
    ws.Range(ws.Cells(2, 1), ws.Cells(lastRow, lastCol)).ClearContents
    ws.Range(ws.Cells(2, 1), ws.Cells(lastRow, lastCol)).Interior.ColorIndex = xlNone
End Sub

' -----------------------------------------------------------------------------
' WriteDataToSheet - Escreve dados na planilha
' -----------------------------------------------------------------------------
Private Function WriteDataToSheet(ws As Worksheet, data As Variant, config As CatalogConfig) As Long
    Dim i As Long, j As Long
    Dim dataRow As Long
    Dim formula As String
    Dim csvCol As Long

    For i = 1 To UBound(data, 1)
        dataRow = i + 1  ' Linha 2 em diante (apos header)

        ' Para FERRAMENTAS, o CSV tem 7 colunas mas a planilha tem 9
        ' CSV: Codigo, Categoria, Descricao, ValorAq, VidaUtil, AtualizadoEm, ValidadeDias
        ' Plan: Codigo, Categoria, Descricao, ValorAq, VidaUtil, CustoHora(F), AtualizadoEm(G), ValidadeDias(H), Selecao(I)
        If config.HasCustoHoraCol Then
            ' Escrever colunas 1-5 do CSV para A-E da planilha
            For j = 1 To 5
                ws.Cells(dataRow, j).Value = data(i, j)
            Next j

            ' Coluna F: CustoHora (formula)
            ws.Cells(dataRow, config.CustoHoraCol).formula = _
                "=IF(E" & dataRow & ">0,D" & dataRow & "/E" & dataRow & ",0)"

            ' Colunas G-H: AtualizadoEm, ValidadeDias (colunas 6-7 do CSV)
            ws.Cells(dataRow, config.AtualizadoEmCol).Value = data(i, 6)
            ws.Cells(dataRow, config.ValidadeDiasCol).Value = data(i, 7)
        Else
            ' Para outros catalogos, escrever colunas de dados diretamente
            For j = 1 To config.NumDataCols
                ws.Cells(dataRow, j).Value = data(i, j)
            Next j
        End If

        ' Adicionar formula de Selecao
        formula = Replace(config.SelectionFormula, "{ROW}", CStr(dataRow))
        ws.Cells(dataRow, config.SelectionCol).formula = formula
    Next i

    WriteDataToSheet = UBound(data, 1) + 1  ' Ultima linha usada
End Function

' -----------------------------------------------------------------------------
' AplicarFormatacaoValidade - Aplica cores baseado na validade por item
' -----------------------------------------------------------------------------
Private Sub AplicarFormatacaoValidade(ws As Worksheet, config As CatalogConfig, lastRow As Long)
    Dim dataRow As Long
    Dim atualizadoEm As Variant
    Dim validadeDias As Variant
    Dim dataExpiracao As Date
    Dim diasRestantes As Long

    For dataRow = 2 To lastRow
        atualizadoEm = ws.Cells(dataRow, config.AtualizadoEmCol).Value
        validadeDias = ws.Cells(dataRow, config.ValidadeDiasCol).Value

        ' Validar dados
        If IsDate(atualizadoEm) Or IsValidDateString(CStr(atualizadoEm)) Then
            On Error Resume Next
            If IsDate(atualizadoEm) Then
                dataExpiracao = CDate(atualizadoEm) + CLng(validadeDias)
            Else
                dataExpiracao = ParseDateString(CStr(atualizadoEm)) + CLng(validadeDias)
            End If
            On Error GoTo 0

            diasRestantes = DateDiff("d", Date, dataExpiracao)

            If diasRestantes < 0 Then
                ' Item vencido - fundo vermelho claro
                ws.Range(ws.Cells(dataRow, 1), ws.Cells(dataRow, config.SelectionCol - 1)).Interior.Color = COLOR_EXPIRED
            ElseIf diasRestantes <= 3 Then
                ' Item expirando - fundo amarelo claro
                ws.Range(ws.Cells(dataRow, 1), ws.Cells(dataRow, config.SelectionCol - 1)).Interior.Color = COLOR_EXPIRING
            Else
                ' Item OK - sem cor
                ws.Range(ws.Cells(dataRow, 1), ws.Cells(dataRow, config.SelectionCol - 1)).Interior.ColorIndex = xlNone
            End If
        End If
    Next dataRow
End Sub

' -----------------------------------------------------------------------------
' IsValidDateString - Verifica se string e data valida (YYYY-MM-DD)
' -----------------------------------------------------------------------------
Private Function IsValidDateString(dateStr As String) As Boolean
    If Len(dateStr) = 10 And Mid(dateStr, 5, 1) = "-" And Mid(dateStr, 8, 1) = "-" Then
        IsValidDateString = True
    Else
        IsValidDateString = False
    End If
End Function

' -----------------------------------------------------------------------------
' ParseDateString - Converte string YYYY-MM-DD para Date
' -----------------------------------------------------------------------------
Private Function ParseDateString(dateStr As String) As Date
    Dim year As Integer, month As Integer, day As Integer

    On Error Resume Next
    year = CInt(Left(dateStr, 4))
    month = CInt(Mid(dateStr, 6, 2))
    day = CInt(Right(dateStr, 2))
    ParseDateString = DateSerial(year, month, day)
    On Error GoTo 0
End Function

' -----------------------------------------------------------------------------
' AtualizarIntervaloNomeadoImport - Atualiza intervalo nomeado
' -----------------------------------------------------------------------------
Private Sub AtualizarIntervaloNomeadoImport(nmName As String, sheetName As String, _
                                            selCol As Integer, lastRow As Long)
    Dim colLetter As String
    Dim refText As String

    colLetter = Split(Cells(1, selCol).Address, "$")(1)
    refText = "=" & sheetName & "!$" & colLetter & "$2:$" & colLetter & "$" & lastRow

    On Error Resume Next
    ThisWorkbook.Names(nmName).Delete
    On Error GoTo 0

    ThisWorkbook.Names.Add Name:=nmName, RefersTo:=refText
End Sub

' -----------------------------------------------------------------------------
' AtualizarTimestamp - Atualiza timestamp da ultima importacao
' -----------------------------------------------------------------------------
Private Sub AtualizarTimestamp()
    Dim ws As Worksheet

    On Error Resume Next
    Set ws = ThisWorkbook.Sheets(CONFIG_SHEET)
    On Error GoTo 0

    If ws Is Nothing Then Exit Sub

    ws.Range(TIMESTAMP_CELL).Value = Format(Now, "dd/mm/yyyy hh:mm:ss")
End Sub

' =============================================================================
' SISTEMA DE VALIDADE POR ITEM
' =============================================================================

' -----------------------------------------------------------------------------
' VerificarValidadeInterna - Verifica validade por item em todos os catalogos
' -----------------------------------------------------------------------------
Private Function VerificarValidadeInterna(showAlerts As Boolean) As String
    Dim catalogos As Variant
    Dim config As CatalogConfig
    Dim ws As Worksheet
    Dim i As Long, dataRow As Long, lastRow As Long
    Dim atualizadoEm As Variant
    Dim validadeDias As Variant
    Dim dataExpiracao As Date
    Dim diasRestantes As Long
    Dim expiredCount As Long
    Dim expiringCount As Long
    Dim expiredItems As String
    Dim expiringItems As String
    Dim totalExpired As Long
    Dim totalExpiring As Long
    Dim wsConfig As Worksheet

    catalogos = Array("MATERIAIS", "MAO_DE_OBRA", "FERRAMENTAS", "EQUIPAMENTOS")
    totalExpired = 0
    totalExpiring = 0
    expiredItems = ""
    expiringItems = ""

    For i = 0 To UBound(catalogos)
        config = GetCatalogConfig(CStr(catalogos(i)))

        On Error Resume Next
        Set ws = ThisWorkbook.Sheets(config.SheetName)
        On Error GoTo 0

        If Not ws Is Nothing Then
            lastRow = ws.Cells(ws.Rows.count, 1).End(xlUp).row
            expiredCount = 0
            expiringCount = 0

            For dataRow = 2 To lastRow
                atualizadoEm = ws.Cells(dataRow, config.AtualizadoEmCol).Value
                validadeDias = ws.Cells(dataRow, config.ValidadeDiasCol).Value

                If IsDate(atualizadoEm) Or IsValidDateString(CStr(atualizadoEm)) Then
                    On Error Resume Next
                    If IsDate(atualizadoEm) Then
                        dataExpiracao = CDate(atualizadoEm) + CLng(validadeDias)
                    Else
                        dataExpiracao = ParseDateString(CStr(atualizadoEm)) + CLng(validadeDias)
                    End If
                    On Error GoTo 0

                    diasRestantes = DateDiff("d", Date, dataExpiracao)

                    If diasRestantes < 0 Then
                        expiredCount = expiredCount + 1
                    ElseIf diasRestantes <= 3 Then
                        expiringCount = expiringCount + 1
                    End If
                End If
            Next dataRow

            If expiredCount > 0 Then
                expiredItems = expiredItems & "- " & catalogos(i) & ": " & expiredCount & " itens" & vbCrLf
                totalExpired = totalExpired + expiredCount
            End If

            If expiringCount > 0 Then
                expiringItems = expiringItems & "- " & catalogos(i) & ": " & expiringCount & " itens" & vbCrLf
                totalExpiring = totalExpiring + expiringCount
            End If
        End If
    Next i

    ' Atualizar status na planilha
    On Error Resume Next
    Set wsConfig = ThisWorkbook.Sheets(CONFIG_SHEET)
    On Error GoTo 0

    If Not wsConfig Is Nothing Then
        If totalExpired > 0 Then
            wsConfig.Range(STATUS_CELL).Value = "VENCIDO (" & totalExpired & ")"
            wsConfig.Range(STATUS_CELL).Font.Color = vbRed
        ElseIf totalExpiring > 0 Then
            wsConfig.Range(STATUS_CELL).Value = "Atencao (" & totalExpiring & ")"
            wsConfig.Range(STATUS_CELL).Font.Color = RGB(255, 165, 0)  ' Laranja
        Else
            wsConfig.Range(STATUS_CELL).Value = "OK"
            wsConfig.Range(STATUS_CELL).Font.Color = RGB(0, 128, 0)  ' Verde
        End If
    End If

    ' Mostrar alertas se solicitado
    If showAlerts Then
        If totalExpired > 0 Then
            MsgBox "ATENCAO: Itens VENCIDOS:" & vbCrLf & vbCrLf & expiredItems & _
                   vbCrLf & "Total: " & totalExpired & " itens" & vbCrLf & vbCrLf & _
                   "Solicite atualizacao ao setor de Suprimentos!", _
                   vbCritical, "Dados Desatualizados"
        ElseIf totalExpiring > 0 Then
            MsgBox "Itens proximos do vencimento:" & vbCrLf & vbCrLf & expiringItems & _
                   vbCrLf & "Total: " & totalExpiring & " itens", _
                   vbExclamation, "Aviso de Validade"
        End If
    End If

    ' Retornar mensagem resumida
    If totalExpired > 0 Then
        VerificarValidadeInterna = "ATENCAO: " & totalExpired & " itens vencidos!"
    ElseIf totalExpiring > 0 Then
        VerificarValidadeInterna = totalExpiring & " itens vencem em breve."
    Else
        VerificarValidadeInterna = ""
    End If
End Function

' -----------------------------------------------------------------------------
' VerificarValidadeAoAbrir - Chamada pelo Workbook_Open
' -----------------------------------------------------------------------------
Public Sub VerificarValidadeAoAbrir()
    Dim msg As String

    On Error Resume Next
    msg = VerificarValidadeInterna(False)
    On Error GoTo 0

    If msg <> "" And InStr(msg, "vencidos") > 0 Then
        MsgBox "ATENCAO: Existem itens com dados vencidos!" & vbCrLf & vbCrLf & _
               msg & vbCrLf & vbCrLf & _
               "Execute 'Verificar Validade' para detalhes.", _
               vbExclamation, "Dados Desatualizados"
    End If
End Sub
