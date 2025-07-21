"""
O módulo random em Python serve para gerar números pseudoaleatórios.
E realizar outras operações relacionadas à aleatoriedade.
"""
import random

class ConjuntoCache:
    """
    Representa um único conjunto dentro da cache, contendo múltiplas vias (linhas).
    Gerencia a lógica de inserção e substituição de blocos de dados.
    """
    def __init__(self, associatividade, politica_substituicao):
        
        self.vias = [{'tag': None, 'valido': False} for _ in range(associatividade)]
        self.politica_substituicao = politica_substituicao
        self.ordem_acesso = []  # Fila para controlar a ordem de uso para LRU e FIFO

    def registrar_acesso(self, tag):
        """
        Processa um acesso a uma tag específica dentro deste conjunto.
        Determina se o acesso resulta em um hit ou um miss.
        """
        # Procura por um hit ou por um espaço vazio (miss compulsório)
        for indice, via in enumerate(self.vias):
            if via['valido']:  # Verifica se a via contém dados válidos
                if via['tag'] == tag:
                    # É um hit!
                    if self.politica_substituicao == 'L':  # Least Recently Used
                        # Move a via acessada para o final da fila para marcar como usada recentemente
                        self.ordem_acesso.remove(indice)
                        self.ordem_acesso.append(indice)
                    return 0  # Código para Hit
            else:
                # É um miss compulsório, pois há um espaço vazio
                via['tag'] = tag
                via['valido'] = True
                self.ordem_acesso.append(indice)
                return 1  # Código para Miss Compulsório

        # Se não houve hit e não há espaços vazios, uma substituição é necessária
        return self.substituir_bloco(tag)

    def substituir_bloco(self, tag):
        """
        Substitui um bloco existente no conjunto usando a política definida.
        Chamado quando o conjunto está cheio e ocorre um miss.
        """
        indice_via_vitima = -1

        if self.politica_substituicao == 'R':  #RANDOM
            indice_via_vitima = random.randint(0, len(self.vias) - 1)
        
        elif self.politica_substituicao in ['F', 'L']:  #FIFO ou LRU
            # Remove a via mais antiga (primeiro elemento da fila)
            indice_via_vitima = self.ordem_acesso.pop(0)
            # Adiciona a nova via (agora a mais recente) ao final da fila
            self.ordem_acesso.append(indice_via_vitima)

        if indice_via_vitima != -1:
            self.vias[indice_via_vitima]['tag'] = tag
            return 2  # Código para Miss de Capacidade/Conflito
        
        return -1  # Retorna -1 em caso de erro na política