def cifrar_vigenere(mensagem, chave):
    mensagem_cifrada = []  # Inicializa uma lista vazia para armazenar os caracteres cifrados
    chave_repetida = chave * (len(mensagem) // len(chave)) + chave[:len(mensagem) % len(chave)]
    # A chave é repetida para corresponder ao tamanho da mensagem

    for i in range(len(mensagem)):  # Percorre cada caractere na mensagem original
        char_mensagem = mensagem[i]  # Obtém o caractere atual da mensagem original
        char_chave = chave_repetida[i]  # Obtém o caractere da chave correspondente

        if char_mensagem.isalpha():  # Verifica se o caractere da mensagem é uma letra
            shift = ord(char_chave.lower()) - ord('a')
            # Calcula o deslocamento com base na letra da chave (converte para minúscula)
            char_base = ord('A') if char_mensagem.isupper() else ord('a')
            # Define a letra base (maiúscula ou minúscula) com base no caractere da mensagem

            char_cifrado = chr(((ord(char_mensagem) - char_base + shift) % 26) + char_base)
            # Calcula o caractere cifrado usando a fórmula da cifra de Vigenère
        else:
            char_cifrado = char_mensagem  # Se não for uma letra, mantém o caractere original

        mensagem_cifrada.append(char_cifrado)  # Adiciona o caractere cifrado à lista

    return ''.join(mensagem_cifrada)  # Converte a lista de caracteres cifrados em uma única string e retorna


def decifrar_vigenere(criptograma, chave):
    mensagem_decifrada = []  # Inicializa uma lista vazia para armazenar os caracteres decifrados
    chave_repetida = chave * (len(criptograma) // len(chave)) + chave[:len(criptograma) % len(chave)]
    # A chave é repetida para corresponder ao tamanho do criptograma

    for i in range(len(criptograma)):  # Percorre cada caractere no criptograma
        char_cifrado = criptograma[i]  # Obtém o caractere atual do criptograma
        char_chave = chave_repetida[i]  # Obtém o caractere da chave correspondente

        if char_cifrado.isalpha():  # Verifica se o caractere do criptograma é uma letra
            shift = ord(char_chave.lower()) - ord('a')
            # Calcula o deslocamento com base na letra da chave (convertida para minúscula)
            char_base = ord('A') if char_cifrado.isupper() else ord('a')
            # Define a letra base (maiúscula ou minúscula) com base no caractere do criptograma

            char_decifrado = chr(((ord(char_cifrado) - char_base - shift) % 26) + char_base)
            # Calcula o caractere decifrado usando a fórmula da cifra de Vigenère
        else:
            char_decifrado = char_cifrado  # Se não for uma letra, mantém o caractere original

        mensagem_decifrada.append(char_decifrado)  # Adiciona o caractere decifrado à lista

    return ''.join(mensagem_decifrada)  # Converte a lista de caracteres decifrados em uma única string e retorna



# Frequências esperadas de letras em português e inglês
frequencias_portugues = {
    'a': 14.63, 'b': 1.04, 'c': 3.88, 'd': 4.99, 'e': 12.57, 'f': 1.02,
    'g': 1.30, 'h': 1.28, 'i': 6.18, 'j': 0.40, 'k': 0.02, 'l': 2.78,
    'm': 4.74, 'n': 4.63, 'o': 9.24, 'p': 2.30, 'q': 1.29, 'r': 6.77,
    's': 7.81, 't': 4.04, 'u': 3.77, 'v': 1.37, 'w': 0.21, 'x': 0.02,
    'y': 0.01, 'z': 0.47
}

frequencias_ingles = {
    'a': 8.17, 'b': 1.49, 'c': 2.78, 'd': 4.25, 'e': 12.70, 'f': 2.23,
    'g': 2.02, 'h': 6.09, 'i': 6.97, 'j': 0.15, 'k': 0.77, 'l': 4.03,
    'm': 2.41, 'n': 6.75, 'o': 7.51, 'p': 1.93, 'q': 0.10, 'r': 5.99,
    's': 6.33, 't': 9.06, 'u': 2.76, 'v': 0.98, 'w': 2.36, 'x': 0.15,
    'y': 1.97, 'z': 0.07
}

def calcular_frequencias(mensagem):
    frequencias = {}  # Inicializa um dicionário para armazenar as frequências das letras
    total_caracteres = 0  # Inicializa uma variável para contar o número total de caracteres na mensagem

    # Loop sobre cada caractere na mensagem
    for char in mensagem:
        if char.isalpha():  # Verifica se o caractere é uma letra (ignorando caracteres não alfabéticos)
            char = char.lower()  # Converte o caractere para minúscula para evitar diferenciação entre maiúsculas e minúsculas
            frequencias[char] = frequencias.get(char, 0) + 1  # Atualiza a contagem de frequência para a letra atual
            total_caracteres += 1  # Incrementa o contador de caracteres totais

    # Calcula as porcentagens de frequência para cada letra
    for char, frequencia in frequencias.items():
        frequencias[char] = (frequencia / total_caracteres) * 100  # Calcula a porcentagem de frequência

    return frequencias  # Retorna o dicionário de frequências


def calcular_correlacao(frequencias_mensagem, frequencias_esperadas):
    total = sum(frequencias_mensagem.values())  # Calcula o total das frequências da mensagem
    correlacao = 0.0  # Inicializa a correlação como 0.0

    # Loop sobre as letras e suas frequências na mensagem
    for letra, frequencia in frequencias_mensagem.items():
        frequencia_esperada = frequencias_esperadas.get(letra, 0)  # Obtém a frequência esperada para a letra atual
        correlacao += (frequencia / total) * frequencia_esperada  # Calcula a contribuição da letra para a correlação

    return correlacao  # Retorna o valor de correlação calculado


def ataque_analise_frequencia(criptograma, frequencias_esperadas):
    # Inicializa a melhor chave encontrada como uma string vazia
    melhor_chave = ""
    # Inicializa a melhor correlação como o pior valor possível
    melhor_correlacao = -1.0

    # Loop sobre as possíveis chaves (todas as letras do alfabeto)
    for chave in range(26):
        chave = chr(ord('a') + chave)  # Converte o índice em uma letra minúscula ('a' a 'z')

        # Decifra o criptograma com a chave atual
        mensagem_decifrada = decifrar_vigenere(criptograma, chave)

        # Calcula as frequências das letras na mensagem decifrada
        frequencias_mensagem = calcular_frequencias(mensagem_decifrada)

        # Calcula a correlação entre as frequências da mensagem decifrada e as frequências esperadas
        correlacao = calcular_correlacao(frequencias_mensagem, frequencias_esperadas)

        # Compara a correlação atual com a melhor correlação encontrada até agora
        if correlacao > melhor_correlacao:
            melhor_correlacao = correlacao  # Atualiza a melhor correlação
            melhor_chave = chave  # Atualiza a melhor chave encontrada até agora

    # Retorna a melhor chave que resultou na maior correlação
    return melhor_chave


# Teste de cifragem e decifragem com uma mensagem simples

mensagem_portugues = "Isso e um teste"
chave_portugues = "chave"  # A chave deve ser "chave" em letras minúsculas

criptograma_portugues = cifrar_vigenere(mensagem_portugues, chave_portugues)
print("Mensagem Cifrada (Português):", criptograma_portugues)

mensagem_decifrada_portugues = decifrar_vigenere(criptograma_portugues, chave_portugues)
print("Mensagem Decifrada (Português):", mensagem_decifrada_portugues)
# Deve imprimir a mensagem original "Isso e um teste"

print('------------------------------------------------')
print('------------------------------------------------')
print('------------------------------------------------')

mensagem_ingles = "This is a test"
chave_ingles = "key"  # A chave deve ser "key" em letras minúsculas

criptograma_ingles = cifrar_vigenere(mensagem_ingles, chave_ingles)
print("Mensagem Cifrada (Inglês):", criptograma_ingles)

mensagem_decifrada_ingles = decifrar_vigenere(criptograma_ingles, chave_ingles)
print("Mensagem Decifrada (Inglês):", mensagem_decifrada_ingles)

print('------------------------------------------------')
print('------------------------------------------------')
print('------------------------------------------------')


# Testes de ataque por análise de frequência para mensagens em português

ataque_mensagem_port = criptograma_portugues
chave_desconhecida_port = ataque_analise_frequencia(ataque_mensagem_port, frequencias_portugues)  # Use frequências em português
print("Chave Recuperada (Português):", chave_desconhecida_port)

mensagem_decifrada_ataque_port = decifrar_vigenere(ataque_mensagem_port, chave_desconhecida_port)
print("Mensagem Decifrada (Ataque - Português):", mensagem_decifrada_ataque_port)

print('------------------------------------------------')

# Testes de ataque por análise de frequência para mensagens em inglês

ataque_mensagem_ing = criptograma_ingles
chave_desconhecida_ing = ataque_analise_frequencia(ataque_mensagem_ing, frequencias_ingles)  # Use frequências em inglês
print("Chave Recuperada (Inglês):", chave_desconhecida_ing)

mensagem_decifrada_ataque = decifrar_vigenere(ataque_mensagem_ing, chave_desconhecida_ing)
print("Mensagem Decifrada (Ataque - Inglês):", mensagem_decifrada_ataque)




