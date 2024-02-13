def transform_bwt(data):
    n = len(data)
    rotations = [data[i:] + data[:i] for i in range(n)]
    sorted_rotations = sorted(rotations)
    transformed_data = ''.join([rotation[-1] for rotation in sorted_rotations])
    key = sorted_rotations.index(data)
    return transformed_data, key

def inverse_bwt(transformed_data, key):
    n = len(transformed_data)
    table = [''] * n

    for _ in range(n):
        table = sorted([transformed_data[i] + table[i] for i in range(n)])
    
    original_data = table[key]
    return original_data

data = "banana"
transformed_data, key = transform_bwt(data)
original_data = inverse_bwt(transformed_data, key)
print("Exemple 1:")
print("Données d'origine:", data)
print("Transformée de Burrows-Wheeler:", transformed_data)
print("Données inversées:", original_data)
print()
