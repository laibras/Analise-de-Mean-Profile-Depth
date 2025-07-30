import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle

def plotar_superficie_analise(dados_circulo, centro_x, centro_y, raio):
    """
    Gera uma figura com a visualização 2D e 3D da área de análise.
    """
    fig = plt.figure(figsize=(12, 6))
    plt.suptitle("Visualização da Superfície de Análise", fontsize=16)

    # --- Gráfico 1: Vista Superior (2D) ---
    ax1 = fig.add_subplot(1, 2, 1)
    # Plota os pontos de dados
    scatter = ax1.scatter(dados_circulo[:, 1], dados_circulo[:, 2], c=dados_circulo[:, 0], cmap='viridis', s=10)
    # Plota o centro e o círculo de análise
    ax1.plot(centro_x, centro_y, 'rx', markersize=10, label='Centro Calculado')
    circulo = Circle((centro_x, centro_y), raio, facecolor='none', edgecolor='red', linestyle='--', label=f'Raio de Análise ({raio} mm)')
    ax1.add_patch(circulo)
    
    ax1.set_xlabel('Eixo X (mm)')
    ax1.set_ylabel('Eixo Y (mm)')
    ax1.set_title('Vista Superior (2D)')
    ax1.legend()
    ax1.axis('equal') # Garante que o círculo não pareça uma elipse
    ax1.grid(True, linestyle=':')
    fig.colorbar(scatter, ax=ax1, label='Altura Z (mm)')

    # --- Gráfico 2: Vista 3D ---
    ax2 = fig.add_subplot(1, 2, 2, projection='3d')
    ax2.scatter(dados_circulo[:, 1], dados_circulo[:, 2], dados_circulo[:, 0], c=dados_circulo[:, 0], cmap='viridis', s=5)
    ax2.set_xlabel('Eixo X (mm)')
    ax2.set_ylabel('Eixo Y (mm)')
    ax2.set_zlabel('Eixo Z (mm)')
    ax2.set_title('Vista da Superfície (3D)')
    
    plt.tight_layout(rect=[0, 0, 1, 0.96])
    plt.show()

def plotar_perfil_individual(dados_plot, n_perfil):
    """
    Gera um gráfico detalhado de um único perfil.
    """
    dist = dados_plot['distancia']
    z_orig = dados_plot['z_original']
    z_trend = dados_plot['z_tendencia']
    z_detrended = dados_plot['z_detrended']

    plt.figure(figsize=(10, 6))
    plt.scatter(dist, z_orig, facecolors='none', edgecolors='blue', label='Dados Originais')
    plt.plot(dist, z_trend, 'r--', label='Linha de Tendência (Inclinação)')
    plt.scatter(dist, z_detrended, color='green', s=15, label='Dados Nivelados (Detrended)')
    plt.axhline(0, color='black', linestyle=':', lw=1, label='Referência Zero')
    
    plt.title(f'Análise Detalhada do Perfil Nº {n_perfil}')
    plt.xlabel('Distância ao Longo do Perfil (mm)')
    plt.ylabel('Altura Z (mm)')
    plt.legend()
    plt.grid(True)
    plt.show()

def calcular_mpd_com_visualizacao(caminho_arquivo, arquivo_saida, raio, n_perfis, tolerancia, perfil_para_visualizar=None):
    """
    Versão principal que calcula o MPD e retorna dados para visualização.
    """
    try:
        dados = np.loadtxt(caminho_arquivo, usecols=(0, 1, 2))
        z, x, y = dados[:, 0], dados[:, 1], dados[:, 2]
    except FileNotFoundError:
        print(f"ERRO: O arquivo de entrada '{caminho_arquivo}' não foi encontrado.")
        return None, None, None
    
    xmin, xmax = np.min(x), np.max(x)
    ymin, ymax = np.min(y), np.max(y)
    centro_x, centro_y = (xmin + xmax) / 2, (ymin + ymax) / 2
    
    distancias_do_centro = np.sqrt((x - centro_x)**2 + (y - centro_y)**2)
    dados_circulo = dados[np.where(distancias_do_centro <= raio)]
    
    if dados_circulo.shape[0] == 0:
        print("Nenhum ponto de dados encontrado dentro do raio especificado.")
        return 0.0, None, None

    lista_mpd_por_perfil = []
    dados_plot_perfil = None # Para armazenar os dados do perfil a ser plotado
    
    with open(arquivo_saida, 'w') as f:
        f.write("Perfil_N;Pico_1_detrend;Pico_2_detrend;Media_Z_detrend;MPD_Perfil\n")
        
        for i in range(n_perfis):
            # ... (cálculos do perfil como antes) ...
            angulo = i * (np.pi / n_perfis)
            vx, vy = np.cos(angulo), np.sin(angulo)
            dx = dados_circulo[:, 1] - centro_x
            dy = dados_circulo[:, 2] - centro_y
            dist_perpendicular = np.abs(vx * dy - vy * dx)
            indices_perfil = np.where(dist_perpendicular <= tolerancia)
            pontos_perfil = dados_circulo[indices_perfil]

            if pontos_perfil.shape[0] < 2:
                continue
            
            dist_ao_longo_do_perfil = (pontos_perfil[:, 1] - centro_x) * vx + (pontos_perfil[:, 2] - centro_y) * vy
            slope, intercept = np.polyfit(dist_ao_longo_do_perfil, pontos_perfil[:, 0], 1)
            linha_tendencia_z = slope * dist_ao_longo_do_perfil + intercept
            z_detrended = pontos_perfil[:, 0] - linha_tendencia_z
            
            # Se este for o perfil que queremos visualizar, salvamos seus dados
            if perfil_para_visualizar is not None and i == perfil_para_visualizar:
                dados_plot_perfil = {
                    'distancia': dist_ao_longo_do_perfil,
                    'z_original': pontos_perfil[:, 0],
                    'z_tendencia': linha_tendencia_z,
                    'z_detrended': z_detrended
                }

            # ... (cálculos do MPD como antes) ...
            media_z_perfil_detrended = np.mean(z_detrended)
            metade1_z_detrended = z_detrended[dist_ao_longo_do_perfil >= 0]
            metade2_z_detrended = z_detrended[dist_ao_longo_do_perfil < 0]
            if metade1_z_detrended.shape[0] > 0 and metade2_z_detrended.shape[0] > 0:
                p1, p2 = np.max(metade1_z_detrended), np.max(metade2_z_detrended)
                mpd_perfil = ((p1 + p2) / 2) - media_z_perfil_detrended
                lista_mpd_por_perfil.append(mpd_perfil)
                f.write(f"{i+1};{p1:.6f};{p2:.6f};{media_z_perfil_detrended:.6f};{mpd_perfil:.6f}\n")

        if not lista_mpd_por_perfil:
            mpd_final = 0.0
        else:
            mpd_final = np.mean(lista_mpd_por_perfil)
            
        f.write(f"\nMPD Final (com detrend);{mpd_final:.6f}\n")

    # Prepara os dados para o plot da superfície
    dados_plot_superficie = {
        'dados_circulo': dados_circulo,
        'centro_x': centro_x,
        'centro_y': centro_y,
        'raio': raio
    }
    
    return mpd_final, dados_plot_superficie, dados_plot_perfil

# --- Bloco Principal de Execução ---
if __name__ == '__main__':
    # --- Parâmetros ajustáveis ---
    NOME_ARQUIVO_ENTRADA = 'cp0.xyz'
    NOME_ARQUIVO_SAIDA = 'resultados_mpd_visual.txt'
    
    RAIO = 40.0
    N_PERFIS = 180
    TOLERANCIA = 0.1
    
    # === CONTROLE DE VISUALIZAÇÃO ===
    # Defina o número do perfil que você quer ver (de 0 a N_PERFIS-1)
    # ou defina como None para não gerar o gráfico do perfil.
    PERFIL_PARA_VISUALIZAR = 150 

    print("Iniciando cálculo de MPD e preparando visualizações...")
    print("----------------------------------------------------")
    
    mpd_resultado, dados_superficie, dados_perfil = calcular_mpd_com_visualizacao(
        NOME_ARQUIVO_ENTRADA, NOME_ARQUIVO_SAIDA, RAIO, N_PERFIS, TOLERANCIA, PERFIL_PARA_VISUALIZAR
    )

    if mpd_resultado is not None:
        print(f"Cálculo concluído. MPD Final: {mpd_resultado:.6f}")
        print(f"Resultados detalhados salvos em '{NOME_ARQUIVO_SAIDA}'")
        print("----------------------------------------------------")
        
        # Gerar os gráficos após o cálculo
        if dados_superficie:
            print("Gerando gráfico da superfície de análise...")
            plotar_superficie_analise(**dados_superficie)
            
        if dados_perfil:
            print(f"Gerando gráfico detalhado do perfil nº {PERFIL_PARA_VISUALIZAR}...")
            plotar_perfil_individual(dados_perfil, PERFIL_PARA_VISUALIZAR)
        
        print("\nAnálise finalizada.")