import heapq

def frequence(data):
    # Initialiser une liste vide pour stocker les fréquences
    frequence = []
    # Parcourir chaque caractère dans le texte
    for caractere in data:
        # Vérifier si le caractère est déjà dans la liste des fréquences
        existe = False
        for i, (freq, char) in enumerate(frequence):
            if char == caractere:
                frequence[i] = (freq + 1, char)
                existe = True
                break
        if not existe:
            frequence.append((1, caractere))
    return frequence

def huffman_tree(frequence):
    feuilles = [(freq, caractere) for freq, caractere in frequence]
    heapq.heapify(feuilles)

    while len(feuilles) > 1:
        gauche = heapq.heappop(feuilles)
        droite = heapq.heappop(feuilles)
        heapq.heappush(feuilles, (gauche[0] + droite[0], gauche[1] + droite[1]))

    return feuilles[0]

def codes(huffman_tree, table=None, prefixe=""):
    if table is None:
        table = {}
    if isinstance(huffman_tree[1], str):
        table[huffman_tree[1]] = prefixe
    else:
        codes(huffman_tree[1][0], table, prefixe + "0")
        codes(huffman_tree[1][1], table, prefixe + "1", prefixe != "")
    return table

def compress_data(data):
    table_de_frequence = frequence(data)
    arbre_huffman = huffman_tree(table_de_frequence)
    
    table_de_codes = codes(arbre_huffman)
    
    donnees_compressées = "".join(str(table_de_codes.get(caractere, "")) for caractere in data)
    
    return donnees_compressées


data = "aabbbccdddd"
compressed_data = compress_data(data)
print("Données compressées:", compressed_data)
