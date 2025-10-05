# Calculadora de Determinante - Escalonamento (Eliminação Gaussiana)

- Selecione a ordem da matriz usando o dropdown no topo
- Uma grade de campos aparece automaticamente no centro da tela
- Digite os elementos da matriz (navegação com Tab/Enter)
- Clique em "Achar Determinante" (botão azul no centro)
- O resultado aparece em destaque e auto-oculta após 5 segundos
animação e auto-oculta após 5 segundos

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