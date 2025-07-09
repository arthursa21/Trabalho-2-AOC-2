"""
O módulo sys fornece acesso a variáveis e funções que interagem com o interpretador Python
e o com o sistema operacional.
"""
import sys
from controlador_cache import ControladorCache

def executar_simulacao():
    """
    Processa os argumentos, executa a simulação da cache e exibe os resultados.
    """
    # Validação dos argumentos da linha de comando
    if len(sys.argv) != 7:
        print("ERRO: Número de argumentos inválido.")
        print("Uso correto: python3 simulador_cache.py <nsets> <bsize> <assoc> <substituição> <flag_saida> <arquivo_de_entrada>")
        sys.exit(1)

    # Leitura e conversão dos parâmetros de entrada
    try:
        num_conjuntos = int(sys.argv[1])
        tam_bloco = int(sys.argv[2])
        associatividade = int(sys.argv[3])
        politica = sys.argv[4].upper()[0]
        flag_saida = int(sys.argv[5])
        arquivo_trace = sys.argv[6]
    except ValueError:
        print("Erro: Os parâmetros numéricos (conjuntos, bloco, assoc, flag) devem ser inteiros.")
        sys.exit(1)


    # Validações de conformidade dos parâmetros
    if not (ControladorCache.eh_potencia_de_dois(num_conjuntos) and ControladorCache.eh_potencia_de_dois(tam_bloco)):
        print("ERRO: O número de conjuntos e o tamanho do bloco devem ser potências de 2.")
        sys.exit(1)

    if politica not in ['R', 'F', 'L']:
        print("ERRO: Política de substituição inválida. Escolha entre 'R' (Random), 'F' (FIFO) ou 'L' (LRU).")
        sys.exit(1)

    if flag_saida not in [0, 1]:
        print("ERRO: Flag de saída inválida. Utilize 0 ou 1.")
        sys.exit(1)

    # Exibição dos parâmetros de simulação configurados
    #print("--- Parâmetros da Simulação de Cache ---")
    #print(f"Número de Conjuntos: {num_conjuntos}")
    #print(f"Tamanho do Bloco: {tam_bloco} bytes")
    #print(f"Associatividade: {associatividade}")
    #print(f"Política de Substituição: {politica}")
    #print(f"Formato de Saída: {flag_saida}")
    #print(f"Arquivo de Trace: {arquivo_trace}")
    #print("----------------------------------------")
    
    # Estrutura para armazenar estatísticas: [hits, miss_comp, miss_cap, miss_conf]
    estatisticas = [0, 0, 0, 0]
    acessos_totais = 0

    # Instanciação do sistema de cache
    sistema_cache = ControladorCache(num_conjuntos, tam_bloco, associatividade, politica)

    try:
        with open(arquivo_trace, 'rb') as arquivo_binario:
            while True:
                # Lê 4 bytes (endereço de 32 bits) do arquivo de trace
                bytes_endereco = arquivo_binario.read(4)
                if not bytes_endereco:
                    break  # Fim do arquivo
                
                endereco_int = int.from_bytes(bytes_endereco, byteorder='big')
                codigo_retorno = sistema_cache.acessar_endereco(endereco_int)

                # Distingue entre miss de capacidade e de conflito
                if codigo_retorno == 2:  # Potencial miss de capacidade ou conflito
                    if not sistema_cache.esta_cheia():
                        codigo_retorno = 3  # É um miss de conflito
                
                estatisticas[codigo_retorno] += 1
                acessos_totais += 1

        total_misses = sum(estatisticas[1:])

        # Exibição dos resultados com base na flag de saída
        if flag_saida == 1:
            taxa_hit = estatisticas[0] / acessos_totais if acessos_totais > 0 else 0
            taxa_miss = total_misses / acessos_totais if acessos_totais > 0 else 0
            taxa_comp = estatisticas[1] / total_misses if total_misses > 0 else 0
            taxa_cap = estatisticas[2] / total_misses if total_misses > 0 else 0
            taxa_conf = estatisticas[3] / total_misses if total_misses > 0 else 0
            print(f"\n{acessos_totais} {taxa_hit:.4f} {taxa_miss:.4f} {taxa_comp:.4f} {taxa_cap:.4f} {taxa_conf:.4f}")
        
        elif flag_saida == 0:
            taxa_hit_percentual = (estatisticas[0] / acessos_totais * 100) if acessos_totais > 0 else 0
            taxa_miss_percentual = (total_misses / acessos_totais * 100) if acessos_totais > 0 else 0
            taxa_comp_percentual = (estatisticas[1] / total_misses * 100) if total_misses > 0 else 0
            taxa_cap_percentual = (estatisticas[2] / total_misses * 100) if total_misses > 0 else 0
            taxa_conf_percentual = (estatisticas[3] / total_misses * 100) if total_misses > 0 else 0

            print("\n--- Resultados da Simulação ---")
            print(f"Arquivo:\t\t{arquivo_trace}")
            print(f"Total de Acessos à Memória:\t{acessos_totais}")
            print(f"Total de Hits:\t\t\t{estatisticas[0]}")
            print(f"Taxa de Hit:\t\t\t{taxa_hit_percentual:.2f}%")
            print(f"Total de Misses:\t\t{total_misses}")
            print(f"Taxa de Miss:\t\t\t{taxa_miss_percentual:.2f}%")
            print("\n--- Detalhamento dos Misses ---")
            print(f"Misses Compulsórios:\t\t{estatisticas[1]} ({taxa_comp_percentual:.2f}%)")
            print(f"Misses de Capacidade:\t\t{estatisticas[2]} ({taxa_cap_percentual:.2f}%)")
            print(f"Misses de Conflito:\t\t{estatisticas[3]} ({taxa_conf_percentual:.2f}%)")
            print("---------------------------------")

    except FileNotFoundError:
        print(f"ERRO: O arquivo '{arquivo_trace}' não foi encontrado.")
    except IOError as e:
        print(f"ERRO: Não foi possível ler o arquivo '{arquivo_trace}'. Detalhes: {e}")

if __name__ == "__main__":
    executar_simulacao()