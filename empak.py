import argparse
import tarfile
import os
from rle import decode_rle
from burrows_wheeler import inverse_bwt

def decompress_file(file_object, output_filename):
    compressed_data = file_object.read()

    # Détecte automatiquement l'algorithme de compression en fonction de l'extension
    file_extension = os.path.splitext(output_filename)[1]
    
    if file_extension == '.rle':
        decompressed_data = decode_rle(compressed_data.decode('utf-8'))
    elif file_extension == '.bwt':
        decompressed_data = inverse_bwt(compressed_data.decode('utf-8'))
    else:
        # Si l'extension n'est pas reconnue, ne rien faire
        return

    # Écrit les données décompressées dans le fichier de sortie
    with open(output_filename, 'w') as file:
        file.write(decompressed_data)

def extract_files(output_archive):
    # Ouvre l'archive tar.gz en mode lecture
    with tarfile.open(output_archive, 'r:gz') as archive:
        for member in archive.getmembers():
            input_filename = member.name
            output_filename = os.path.splitext(input_filename)[0]

            # Extrait le fichier compressé et le décompresse
            file_object = archive.extractfile(member)
            decompress_file(file_object, output_filename)

def main():
    # Configuration de l'analyseur d'arguments en ligne de commande
    parser = argparse.ArgumentParser(description='Empaktor - Outil de compression et de décompression')
    parser.add_argument('--extract', type=str, help='Nom de l\'archive compressée à extraire')

    # Analyse des arguments de la ligne de commande
    args = parser.parse_args()
    output_archive = args.extract

    # Vérifie si l'option d'extraction est spécifiée
    if output_archive:
        extract_files(output_archive)
    else:
        print("Veuillez spécifier l'archive à extraire avec l'option --extract.")

if __name__ == "__main__":
    main()