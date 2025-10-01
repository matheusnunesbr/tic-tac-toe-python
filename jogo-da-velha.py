import math

JOGADOR_HUMANO = 'X'
JOGADOR_IA = 'O'

def imprimir_tabuleiro(tabuleiro):
    "Função para exibir o tabuleiro formatado no console."
    print("\n")
    for i in range(0, 9, 3):
        print(f" {tabuleiro[i]} | {tabuleiro[i+1]} | {tabuleiro[i+2]} ")
        if i < 6:
            print("---|---|---")
    print("\n")

def verificar_vencedor(tabuleiro, jogador):
    "Verifica se um jogador venceu o jogo."
    combinacoes_vitoria = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8], 
        [0, 3, 6], [1, 4, 7], [2, 5, 8],  
        [0, 4, 8], [2, 4, 6]             
    ]
    for combo in combinacoes_vitoria:
        if all(tabuleiro[i] == jogador for i in combo):
            return True
    return False

def tabuleiro_cheio(tabuleiro):
    "Verifica se o tabuleiro está completamente preenchido (empate)."
    return all(pos != ' ' for pos in tabuleiro)

def movimentos_disponiveis(tabuleiro):
    "Retorna uma lista de posições vazias no tabuleiro."
    return [i for i, pos in enumerate(tabuleiro) if pos == ' ']

def minimax(tabuleiro, profundidade, eh_maximizador):
    """
    - tabuleiro: o estado atual do jogo.
    - profundidade: o quão fundo na árvore de decisões estamos.
    - eh_maximizador: booleano que indica se é a vez do jogador que maximiza (IA) ou minimiza (Humano).
    """
    #Verifica se o jogo terminou
    if verificar_vencedor(tabuleiro, JOGADOR_IA):
        return 10 - profundidade  # IA venceu. Se Valor == valor positivo: bom para a IA.
    if verificar_vencedor(tabuleiro, JOGADOR_HUMANO):
        return profundidade - 10  # Humano venceu. Se Valor == valor negativo: ruim para a IA.
    if tabuleiro_cheio(tabuleiro):
        return 0  # Empate.

    #Passo recursivo
    if eh_maximizador:  # Turno da IA (quer o maior score)
        melhor_score = -math.inf
        for movimento in movimentos_disponiveis(tabuleiro):
            tabuleiro[movimento] = JOGADOR_IA
            score = minimax(tabuleiro, profundidade + 1, False)
            tabuleiro[movimento] = ' ' # Desfaz o movimento
            melhor_score = max(score, melhor_score)
        return melhor_score
    else:  # Turno do Humano (IA assume que ele fará a melhor jogada para si, ou seja, o menor score)
        melhor_score = math.inf
        for movimento in movimentos_disponiveis(tabuleiro):
            tabuleiro[movimento] = JOGADOR_HUMANO
            score = minimax(tabuleiro, profundidade + 1, True)
            tabuleiro[movimento] = ' ' # Desfaz o movimento
            melhor_score = min(score, melhor_score)
        return melhor_score

def encontrar_melhor_jogada(tabuleiro):
    """
    Função que a IA usa para decidir qual movimento fazer.
    Ela testa todos os movimentos possíveis e escolhe aquele que leva ao maior score retornado pelo minimax.
    """
    melhor_score = -math.inf
    melhor_jogada = -1

    for movimento in movimentos_disponiveis(tabuleiro):
        tabuleiro[movimento] = JOGADOR_IA
        score = minimax(tabuleiro, 0, False) # Chama o minimax para o oponente (humano)
        tabuleiro[movimento] = ' ' # Desfaz o movimento

        if score > melhor_score:
            melhor_score = score
            melhor_jogada = movimento
    
    return melhor_jogada

def jogo():
    "Função principal que executa o loop do jogo."
    tabuleiro = [' ' for _ in range(9)]
    print("Bem-vindo ao Jogo da Velha com IA!")
    print("Você é 'X'. Para jogar, digite um número de 0 a 8.")
    
    # Exibe o tabuleiro de referência
    imprimir_tabuleiro([str(i) for i in range(9)])
    print("Comece o jogo!")

    while True:
        # --- Turno do Humano ---
        imprimir_tabuleiro(tabuleiro)
        movimento_humano = -1
        while movimento_humano == -1:
            try:
                pos = int(input("Sua vez. Escolha uma posição (0-8): "))
                if 0 <= pos <= 8 and tabuleiro[pos] == ' ':
                    movimento_humano = pos
                else:
                    print("Posição inválida ou já ocupada. Tente novamente.")
            except ValueError:
                print("Entrada inválida. Por favor, digite um número.")

        tabuleiro[movimento_humano] = JOGADOR_HUMANO

        if verificar_vencedor(tabuleiro, JOGADOR_HUMANO):
            imprimir_tabuleiro(tabuleiro)
            print("Parabéns! Você venceu!")
            break
        
        if tabuleiro_cheio(tabuleiro):
            imprimir_tabuleiro(tabuleiro)
            print("Deu empate!")
            break

        # --- Turno da IA ---
        print("Vez do computador...")
        movimento_ia = encontrar_melhor_jogada(tabuleiro)
        if movimento_ia != -1:
            tabuleiro[movimento_ia] = JOGADOR_IA

        if verificar_vencedor(tabuleiro, JOGADOR_IA):
            imprimir_tabuleiro(tabuleiro)
            print("A IA venceu! Tente novamente.")
            break
            
        if tabuleiro_cheio(tabuleiro):
            imprimir_tabuleiro(tabuleiro)
            print("Deu empate!")
            break

# Inicia o jogo
if __name__ == "__main__":
    jogo()