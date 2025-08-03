
# Análise de Mean Profile Depth (MPD) para Dados XYZ

Este projeto contém uma coleção de scripts em Python para calcular a Profundidade Média de Perfil (MPD), um parâmetro chave na metrologia de superfícies, a partir de arquivos de dados de coordenadas no formato XYZ. As ferramentas foram desenvolvidas para oferecer flexibilidade na análise, incluindo diferentes metodologias de perfilamento, remoção de inclinação e visualização de dados.

## 🎯 Principais Funcionalidades

  * **Análise por Perfis Radiais**: Calcula o MPD traçando perfis que se irradiam a partir do centro da amostra.
  * **Análise por Perfis Verticais**: Executa a análise em uma grade retilínea, simulando o comportamento de um perfilômetro de contato.
  * **Remoção de Inclinação (Detrending)**: Utiliza regressão linear em cada perfil para remover a forma ou inclinação geral da amostra, isolando a rugosidade e a ondulação para um cálculo de MPD mais preciso.
  * **Geração de Relatórios**: Salva os resultados detalhados de cada perfil (picos, média, MPD do perfil) em um arquivo de texto (`.txt`) para análise posterior.
  * **Visualização de Dados**: Gera gráficos 2D e 3D da área de análise e dos perfis individuais, utilizando `matplotlib` para facilitar a interpretação dos resultados e a validação dos parâmetros.
  * **Configuração Flexível**: Permite ajustar facilmente os principais parâmetros da análise, como raio da amostra e tolerância do perfil.

## 📁 Estrutura do Projeto

  * `mpd_radial_visual.py`: Script para análise via perfis radiais, com detrending e visualização.
  * `mpd_vertical_visual.py`: Script para análise via perfis verticais em um quadrado inscrito, com detrending e visualização.
  * `cp0.xyz`: Arquivo de exemplo com dados de coordenadas.
  * `README.md`: Este arquivo.

## 🚀 Como Usar

Siga os passos abaixo para configurar e executar a análise em seus próprios dados.

### 1\. Pré-requisitos

Certifique-se de ter o Python 3.9 ou superior instalado. Você também precisará das seguintes bibliotecas:

  * **NumPy**: Para cálculos numéricos eficientes.
  * **Matplotlib**: Para a geração dos gráficos de visualização.

### 2\. Instalação

1.  **Clone o repositório (ou baixe os arquivos):**

    ```bash
    git clone https://github.com/SEU-USUARIO/SEU-REPOSITORIO.git
    cd SEU-REPOSITORIO
    ```

2.  **Instale as dependências:**
    Recomenda-se o uso de um ambiente virtual para evitar conflitos de pacotes.

    ```bash
    # Cria um ambiente virtual (opcional, mas recomendado)
    python -m venv venv
    # Ativa o ambiente (Windows)
    .\venv\Scripts\activate
    # Ativa o ambiente (macOS/Linux)
    source venv/bin/activate

    # Instala as bibliotecas necessárias
    pip install numpy matplotlib
    ```

### 3\. Execução

1.  **Prepare seu arquivo de dados:**

      * Certifique-se de que seu arquivo de dados (`.xyz` ou `.txt`) tenha as colunas na seguinte ordem: **Z, X, Y**, e o restante será ignorado.
      * Coloque seu arquivo de dados na mesma pasta dos scripts.

2.  **Configure o Script:**

      * Abra o script que deseja usar (ex: `mpd_vertical_visual.py`).
      * No bloco `if __name__ == '__main__':` no final do arquivo, ajuste os parâmetros:
        ```python
        # --- Parâmetros ajustáveis ---
        NOME_ARQUIVO_ENTRADA = 'seus_dados.xyz'  # <-- Altere para o nome do seu arquivo
        NOME_ARQUIVO_SAIDA = 'resultados_analise.txt' # Nome do arquivo de resultados

        RAIO = 40.0         # Raio da área de análise (em mm)
        TOLERANCIA = 0.2    # Largura/resolução dos perfis (em mm)

        # Parâmetro de visualização (se aplicável)
        PERFIL_PARA_VISUALIZAR = 45 
        ```

3.  **Execute o Script no Terminal:**

    ```bash
    python mpd_vertical_visual.py
    ```

## 📈 Saídas do Programa

Após a execução, o programa irá:

1.  **Imprimir o MPD final no console.**
2.  **Salvar um arquivo de texto** (ex: `resultados_analise.txt`) com os dados detalhados de cada perfil analisado.
3.  **Exibir janelas de gráfico** com as visualizações da superfície e/ou dos perfis, se a função estiver habilitada.

## 🔬 Metodologias

Este projeto implementa duas abordagens distintas para o perfilamento:

1.  **Perfis Radiais**: Ideal para superfícies com características isotrópicas (comportamento similar em todas as direções) ou para análises focadas no centro de uma amostra.
2.  **Perfis Verticais (Grade Retilínea)**: Simula uma varredura mecânica e é excelente para detectar anisotropia (características direcionais) na textura da superfície.

A comparação dos resultados entre os dois métodos pode fornecer insights valiosos sobre a direcionalidade da superfície analisada.

## Autor

Jose Roberto

## 📄 Licença

Este projeto está sob a licença [MIT](https://choosealicense.com/licenses/mit/).
