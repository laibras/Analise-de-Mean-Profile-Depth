import numpy as np

def calcular_mpd_avancado(caminho_arquivo, arquivo_saida, raio, n_perfis, tolerancia):
    """
    Calcula o MPD com remoção de inclinação (detrending) em cada perfil 
    e gera um arquivo de saída com resultados detalhados.

    Argumentos:
        caminho_arquivo (str): Caminho para o arquivo de dados de entrada.
        arquivo_saida (str): Nome do arquivo de texto para salvar os resultados.
        raio (float): Raio do círculo de análise.
        n_perfis (int): Número de perfis radiais.
        tolerancia (float): Tolerância para agrupar pontos em um perfil.

    Retorna:
        float: O valor final do MPD, ou None se ocorrer um erro.
    """
    try:
        dados = np.loadtxt(caminho_arquivo, usecols=(0, 1, 2))
        z, x, y = dados[:, 0], dados[:, 1], dados[:, 2]
    except FileNotFoundError:
        print(f"ERRO: O arquivo de entrada '{caminho_arquivo}' não foi encontrado.")
        return None
    except Exception as e:
        print(f"Ocorreu um erro ao ler o arquivo de entrada: {e}")
        return None

    xmin, xmax = np.min(x), np.max(x)
    ymin, ymax = np.min(y), np.max(y)
    centro_x, centro_y = (xmin + xmax) / 2, (ymin + ymax) / 2
    
    print(f"Centro da amostra (X, Y) calculado: ({centro_x:.4f}, {centro_y:.4f})")

    distancias_do_centro = np.sqrt((x - centro_x)**2 + (y - centro_y)**2)
    dados_circulo = dados[np.where(distancias_do_centro <= raio)]
    
    if dados_circulo.shape[0] == 0:
        print("Nenhum ponto de dados encontrado dentro do raio especificado.")
        return 0.0

    print(f"{dados_circulo.shape[0]} pontos de dados estão dentro do raio para análise.")

    lista_mpd_por_perfil = []
    
    with open(arquivo_saida, 'w') as f:
        f.write("Perfil_N;Pico_1_detrend;Pico_2_detrend;Media_Z_detrend;MPD_Perfil\n")

        for i in range(n_perfis):
            angulo = i * (np.pi / n_perfis)
            vx, vy = np.cos(angulo), np.sin(angulo)

            dx = dados_circulo[:, 1] - centro_x
            dy = dados_circulo[:, 2] - centro_y
            
            dist_perpendicular = np.abs(vx * dy - vy * dx)
            indices_perfil = np.where(dist_perpendicular <= tolerancia)
            pontos_perfil = dados_circulo[indices_perfil]

            if pontos_perfil.shape[0] < 2:
                continue
            
            # --- ETAPA DE REMOÇÃO DA INCLINAÇÃO (DETREND) ---
            # 1. Calcular a posição de cada ponto ao longo da linha do perfil (nosso eixo X para a regressão)
            dist_ao_longo_do_perfil = (pontos_perfil[:, 1] - centro_x) * vx + (pontos_perfil[:, 2] - centro_y) * vy
            
            # 2. Fazer a regressão linear (polinômio de grau 1)
            # A função retorna os coeficientes [slope, intercept] da linha de tendência
            slope, intercept = np.polyfit(dist_ao_longo_do_perfil, pontos_perfil[:, 0], 1)
            
            # 3. Calcular a linha de tendência para cada ponto
            linha_tendencia_z = slope * dist_ao_longo_do_perfil + intercept
            
            # 4. Subtrair a tendência para "nivelar" o perfil
            z_detrended = pontos_perfil[:, 0] - linha_tendencia_z
            # ---------------------------------------------------

            # A partir daqui, usamos apenas os valores Z "nivelados" (z_detrended)
            media_z_perfil_detrended = np.mean(z_detrended)
            
            # Dividir o perfil em duas metades
            metade1_z_detrended = z_detrended[dist_ao_longo_do_perfil >= 0]
            metade2_z_detrended = z_detrended[dist_ao_longo_do_perfil < 0]

            if metade1_z_detrended.shape[0] > 0 and metade2_z_detrended.shape[0] > 0:
                p1 = np.max(metade1_z_detrended)
                p2 = np.max(metade2_z_detrended)
                
                # O MPD é calculado sobre os dados já nivelados
                mpd_perfil = ((p1 + p2) / 2) - media_z_perfil_detrended
                lista_mpd_por_perfil.append(mpd_perfil)
                
                f.write(f"{i+1};{p1:.6f};{p2:.6f};{media_z_perfil_detrended:.6f};{mpd_perfil:.6f}\n")

        if not lista_mpd_por_perfil:
            print("\nAviso: Não foi possível calcular o MPD para nenhum perfil.")
            f.write("\nNenhum perfil válido encontrado com os parâmetros atuais.\n")
            return 0.0

        mpd_final = np.mean(lista_mpd_por_perfil)
        
        f.write("\n\n--- RESULTADO FINAL ---\n")
        f.write(f"MPD Final (com detrend);{mpd_final:.6f}\n")

    print(f"\nArquivo de resultados avançados foi salvo como '{arquivo_saida}'")
    
    return mpd_final

# --- Bloco Principal de Execução ---
if __name__ == '__main__':
    # --- Parâmetros ajustáveis ---
    NOME_ARQUIVO_ENTRADA = 'cp0.xyz'
    NOME_ARQUIVO_SAIDA = 'resultados_mpd_cp0_linear_t.txt' # Novo nome para o arquivo de saída

    RAIO = 40.0
    N_PERFIS = 180
    TOLERANCIA = 0.005

    print("Iniciando cálculo de MPD (versão avançada com remoção de inclinação)...")
    print("-----------------------------------------------------------------------")
    
    mpd_resultado = calcular_mpd_avancado(NOME_ARQUIVO_ENTRADA, NOME_ARQUIVO_SAIDA, RAIO, N_PERFIS, TOLERANCIA)

    if mpd_resultado is not None:
        print("-----------------------------------------------------------------------")
        print("\n--- RESULTADO ---")
        print(f"O MPD final (com remoção de inclinação) é: {mpd_resultado:.6f}")