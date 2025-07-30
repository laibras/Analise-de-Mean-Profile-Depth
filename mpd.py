import numpy as np

def calcular_mpd(caminho_arquivo, arquivo_saida, raio, n_perfis, tolerancia):
    """
    Calcula o MPD e gera um arquivo de saída com resultados detalhados.

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

    # Encontrar o centro usando os MÁXIMOS e MÍNIMOS de X e Y
    xmin, xmax = np.min(x), np.max(x)
    ymin, ymax = np.min(y), np.max(y)
    centro_x, centro_y = (xmin + xmax) / 2, (ymin + ymax) / 2
    
    print(f"Centro da amostra (X, Y) calculado: ({centro_x:.4f}, {centro_y:.4f})")

    # Filtrar pontos dentro do raio
    distancias_do_centro = np.sqrt((x - centro_x)**2 + (y - centro_y)**2)
    dados_circulo = dados[np.where(distancias_do_centro <= raio)]
    
    if dados_circulo.shape[0] == 0:
        print("Nenhum ponto de dados encontrado dentro do raio especificado.")
        return 0.0

    print(f"{dados_circulo.shape[0]} pontos de dados estão dentro do raio para análise.")

    lista_mpd_por_perfil = []
    
    # Abrir o arquivo de saída para escrita
    with open(arquivo_saida, 'w') as f:
        # Escrever o cabeçalho no arquivo
        f.write("Perfil_N;Pico_1;Pico_2;Media_Z_Perfil;MPD_Perfil\n")

        # Loop através dos perfis
        for i in range(n_perfis):
            angulo = i * (np.pi / n_perfis)
            vx, vy = np.cos(angulo), np.sin(angulo)

            dx = dados_circulo[:, 1] - centro_x
            dy = dados_circulo[:, 2] - centro_y
            
            dist_perpendicular = np.abs(vx * dy - vy * dx)
            pontos_perfil = dados_circulo[np.where(dist_perpendicular <= tolerancia)]

            if pontos_perfil.shape[0] < 2:
                continue
            
            media_z_perfil = np.mean(pontos_perfil[:, 0])
            
            produto_escalar = (pontos_perfil[:, 1] - centro_x) * vx + (pontos_perfil[:, 2] - centro_y) * vy
            
            metade1_pontos = pontos_perfil[produto_escalar >= 0]
            metade2_pontos = pontos_perfil[produto_escalar < 0]

            if metade1_pontos.shape[0] > 0 and metade2_pontos.shape[0] > 0:
                p1 = np.max(metade1_pontos[:, 0])
                p2 = np.max(metade2_pontos[:, 0])
                mpd_perfil = ((p1 + p2) / 2) - media_z_perfil
                lista_mpd_por_perfil.append(mpd_perfil)
                
                # Escrever os dados do perfil no arquivo
                # Usando i+1 para que o número do perfil comece em 1
                f.write(f"{i+1};{p1:.6f};{p2:.6f};{media_z_perfil:.6f};{mpd_perfil:.6f}\n")

        if not lista_mpd_por_perfil:
            print("\nAviso: Não foi possível calcular o MPD para nenhum perfil.")
            f.write("\nNenhum perfil válido encontrado com os parâmetros atuais.\n")
            return 0.0

        mpd_final = np.mean(lista_mpd_por_perfil)
        
        # Escrever o resultado final no arquivo
        f.write("\n\n--- RESULTADO FINAL ---\n")
        f.write(f"MPD Final;{mpd_final:.6f}\n")

    print(f"\nArquivo de resultados detalhados foi salvo como '{arquivo_saida}'")
    
    return mpd_final

# --- Bloco Principal de Execução ---
if __name__ == '__main__':
    # --- Parâmetros ajustáveis ---

    # 1. DEFINA OS NOMES DOS ARQUIVOS DE ENTRADA E SAÍDA
    NOME_ARQUIVO_ENTRADA = 'cp0.xyz'  # <-- Altere para o nome do seu arquivo de dados
    NOME_ARQUIVO_SAIDA = 'resultados_mpd_cp0.txt' # <-- Nome do arquivo de resultados

    # 2. AJUSTE OS PARÂMETROS DE CÁLCULO SE NECESSÁRIO
    RAIO = 40.0
    N_PERFIS = 180
    TOLERANCIA = 0.1

    print("Iniciando cálculo de MPD...")
    print("---------------------------------")
    
    mpd_resultado = calcular_mpd(NOME_ARQUIVO_ENTRADA, NOME_ARQUIVO_SAIDA, RAIO, N_PERFIS, TOLERANCIA)

    if mpd_resultado is not None:
        print("---------------------------------")
        print("\n--- RESULTADO ---")
        print(f"O MPD final calculado é: {mpd_resultado:.6f}")