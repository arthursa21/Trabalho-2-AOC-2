from conjunto_cache import ConjuntoCache

class ControladorCache:
    """
    Define a estrutura e o comportamento geral da cache.
    Esta classe coordena os conjuntos e processa os endereços de memória.
    """
    def __init__(self, num_conjuntos, tam_bloco, associatividade, politica_subst):
        """
        Inicializa o controlador da cache.
        
        Argumentos:
        """
        self.num_conjuntos = num_conjuntos # Número de conjuntos na cache
        self.tam_bloco = tam_bloco # Tamanho do bloco de dados em bytes
        self.associatividade = associatividade # Número de vias (linhas) por conjunto
        self.politica_subst = politica_subst # Política de substituição ('R' para Random, 'F' para FIFO, 'L' para LRU)
        
        # Cria a estrutura da cache como uma lista de objetos ConjuntoCache
        self.conjuntos = [ConjuntoCache(associatividade, politica_subst) for _ in range(num_conjuntos)]
        # Calcula o número total de linhas (vias) disponíveis na cache
        self.total_linhas_cache = num_conjuntos * associatividade
        # Contador para o número de linhas atualmente ocupadas
        self.linhas_ocupadas = 0

    def acessar_endereco(self, endereco):
        """
        Processa um acesso à memória, decodificando o endereço para encontrar
        a tag e o índice do conjunto correspondente.
        """
        # Calcula o número de bits para o offset e para o índice
        bits_offset = self.tam_bloco.bit_length() - 1
        bits_indice = self.num_conjuntos.bit_length() - 1

        # Extrai a tag e o índice do endereço
        tag = endereco >> (bits_offset + bits_indice)
        mascara_indice = (1 << bits_indice) - 1
        indice = (endereco >> bits_offset) & mascara_indice

        # Realiza a operação de acesso no conjunto apropriado
        resultado = self.conjuntos[indice].registrar_acesso(tag)

        # Se for um miss compulsório, significa que uma nova linha foi ocupada
        if resultado == 1:
            self.linhas_ocupadas += 1

        return resultado

    def esta_cheia(self):
        """Verifica se todas as linhas da cache estão ocupadas."""
        return self.linhas_ocupadas >= self.total_linhas_cache

    @staticmethod
    def eh_potencia_de_dois(numero):
        """Método estático para verificar se um número é uma potência de 2."""
        return numero > 0 and (numero & (numero - 1)) == 0