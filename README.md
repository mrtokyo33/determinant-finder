# Calculadora de Determinante - Escalonamento (Eliminação Gaussiana)

Uma aplicação Python com interface gráfica moderna (PyQt5) para calcular determinantes de matrizes usando o método de escalonamento (eliminação gaussiana), seguindo os princípios de Clean Architecture.

## Características

- ✅ **Interface PyQt5 moderna** - Visual profissional com tema escuro
- ✅ **Tema escuro com destaque azul** - Fundo escuro com acentos azuis vibrantes
- ✅ **Botões sem bordas** - Design minimalista e moderno
- ✅ **Seleção por dropdown** - Ordem da matriz de 2x2 até 10x10
- ✅ **Grade de matriz centralizada** - Campos de entrada com tema escuro
- ✅ **Resultado em destaque** - Aparece com animação e auto-oculta
- ✅ **Cálculo por escalonamento** - Método mais eficiente computacionalmente
- ✅ **Arquitetura limpa** - Separação de responsabilidades

## Estrutura do Projeto (Clean Architecture)

```
determinante/
├── entities/                    # Camada de Entidades
│   ├── __init__.py
│   ├── matrix.py               # Entidade Matrix
│   └── determinant_calculator.py # Calculadora de Determinante
├── use_cases/                  # Camada de Casos de Uso
│   ├── __init__.py
│   └── calculate_determinant_use_case.py
├── interfaces/                 # Camada de Interface
│   ├── __init__.py
│   └── gui.py                  # Interface Gráfica
├── main.py                     # Ponto de entrada da aplicação
└── README.md                   # Este arquivo
```

## Como Executar

1. **Pré-requisitos:**
   - Python 3.7 ou superior
   - PyQt5 (instalado automaticamente via requirements.txt)

2. **Executar a aplicação:**
   ```bash
   python main.py
   ```

3. **Usar a aplicação:**
   - Selecione a ordem da matriz usando o dropdown no topo
   - Uma grade de campos aparece automaticamente no centro da tela
   - Digite os elementos da matriz (navegação com Tab/Enter)
   - Clique em "Achar Determinante" (botão azul no centro)
   - O resultado aparece em destaque e auto-oculta após 5 segundos

## Funcionalidades

### Interface Gráfica
- **PyQt5 Moderno**: Interface nativa com tema escuro profissional
- **Tema Escuro com Destaque Azul**: Fundo escuro com acentos azuis vibrantes
- **Botões Sem Bordas**: Design minimalista e moderno
- **Seleção por Dropdown**: Menu suspenso para escolher ordem da matriz (2-10)
- **Grade Centralizada**: Campos com tema escuro e navegação por Tab/Enter
- **Resultado em Destaque**: Aparece com animação e auto-oculta após 5 segundos

### Algoritmo
- **Escalonamento (Eliminação Gaussiana)**: Método mais eficiente computacionalmente
- **Pivoteamento Parcial**: Seleciona o maior elemento da coluna como pivô
- **Eliminação por Linhas**: Zera elementos abaixo da diagonal principal
- **Matriz Triangular**: Converte para forma triangular superior
- **Produto da Diagonal**: Determinante é o produto dos elementos da diagonal

### Logging
- **Arquivo de Log**: `determinant_calculator.log`
- **Console Output**: Logs também aparecem no console
- **Níveis de Log**: DEBUG, INFO, WARNING, ERROR
- **Detalhamento**: Logs de cada passo do cálculo

## Exemplo de Uso

1. Execute `python main.py`
2. Selecione ordem 3 para uma matriz 3x3
3. Clique "Criar Matriz"
4. Digite os elementos, por exemplo:
   ```
   1  2  3
   4  5  6
   7  8  9
   ```
5. Clique "Calcular Determinante"
6. Veja o resultado: 0 (matriz singular)

## Logs

O sistema gera logs detalhados incluindo:
- Criação da matriz
- Validação dos dados
- Cada passo do escalonamento
- Troca de linhas (pivoteamento)
- Eliminação de elementos
- Matriz triangular resultante
- Cálculo do produto da diagonal
- Resultado final

## Arquitetura

A aplicação segue os princípios de Clean Architecture:

- **Entities**: Contêm as regras de negócio fundamentais (Matrix, DeterminantCalculator)
- **Use Cases**: Orquestram o fluxo da aplicação (CalculateDeterminantUseCase)
- **Interfaces**: Implementam a interface com o usuário (GUI)
- **Main**: Ponto de entrada que conecta todas as camadas

Esta separação garante:
- Testabilidade
- Manutenibilidade
- Flexibilidade
- Independência de frameworks
