def encode_rle(data):
    encoded_data = ""
    i = 0

    # Parcourir la chaîne d'entrée
    while i < len(data):
        compt = 1
        lettre = data[i]
        j = i

        # Compter les répétitions de la lettre actuelle
        while j < len(data) - 1:
            if data[j] == data[j + 1]:
                compt += 1
                j += 1
            else:
                break

        encoded_data = encoded_data + str(compt) + lettre
        i = j + 1

    return encoded_data


def decode_rle(encoded_data):
    decoded_data = ""
    i = 0

    while i < len(encoded_data):
        count_str = ""
        # Trouver le nombre de répétitions
        while i < len(encoded_data) and encoded_data[i].isdigit():
            count_str += encoded_data[i]
            i += 1

        count = int(count_str) if count_str else 1  # Si count_str est vide, comptez 1

        # Récupérer la lettre correspondante
        if i < len(encoded_data):
            letter = encoded_data[i]
            decoded_data += count * letter
            i += 1

    return decoded_data

data = "AAABBBCCD"
encoded_data = encode_rle(data)
decoded_data = decode_rle(encoded_data)
print("Exemple 1:")
print("Données d'origine:", data)
print("Données encodées:", encoded_data)
print("Données décodées:", decoded_data)
print()