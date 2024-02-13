import argparse
import tarfile
import os
from rle import encode_rle, decode_rle
from huffman import compress_data
from burrows_wheeler import transform_bwt, inverse_bwt

def compress_file(input_filename, output_filename, algorithm):
    # Ouvre le fichier en lecture
    with open(input_filename, 'r') as file:
        data = file.read()

    # Choix de l'algorithme de compression en fonction du paramètre
    if algorithm == 'rle':
        compressed_data = encode_rle(data).encode('utf-8')
    elif algorithm == 'huffman':
        compressed_data = compress_data(data).encode('utf-8')
    elif algorithm == 'bwt':
        transformed_data, _ = transform_bwt(data)  # Déballe le tuple et ignore la clé
        compressed_data = transformed_data.encode('utf-8')

    # Écrit les données compressées dans le fichier de sortie
    with open(output_filename, 'wb') as file:
        file.write(compressed_data)

def decompress_file(file_object, output_filename, compression_algorithm):
    compressed_data = file_object.read()

    # Détecte automatiquement l'algorithme de compression en fonction de l'extension
    file_extension = os.path.splitext(output_filename)[1]
    
    if compression_algorithm == 'rle':
        decompressed_data = decode_rle(compressed_data.decode('utf-8'))
    elif compression_algorithm == 'bwt':
        decompressed_data = inverse_bwt(compressed_data.decode('utf-8'))
    else:
        # Si l'extension n'est pas reconnue, ne rien faire
        return

    # Écrit les données décompressées dans le fichier de sortie
    with open(output_filename, 'w') as file:
        file.write(decompressed_data)

def process_files(input_files, output_archive, compression_algorithm, operation):
    if operation == 'compress':
        # Crée une archive tar.gz et y ajoute les fichiers compressés
        with tarfile.open(output_archive, 'w:gz') as archive:
            for input_file in input_files:
                compressed_file = f"{input_file}.{compression_algorithm}"
                compress_file(input_file, compressed_file, compression_algorithm)
                archive.add(compressed_file)
    elif operation == 'extract':
        # Ouvre l'archive tar.gz en mode lecture
        with tarfile.open(output_archive, 'r:gz') as archive:
            for member in archive.getmembers():
                input_filename = member.name
                output_filename = os.path.splitext(input_filename)[0]
                file_extension = os.path.splitext(input_filename)[1]
                
                # Vérifie si l'extension correspond à l'algorithme de compression
                if file_extension == f'.{compression_algorithm}':
                    # Extrait le fichier compressé et le décompresse
                    file_object = archive.extractfile(member)
                    decompress_file(file_object, output_filename, compression_algorithm)

def main():
    # Configuration de l'analyseur d'arguments en ligne de commande
    parser = argparse.ArgumentParser(description='Empaktor - Outil de compression et de décompression')
    parser.add_argument('output_archive', type=str, help='Le nom de l\'archive compressée')
    parser.add_argument('--compression', type=str, choices=['rle', 'huffman', 'bwt'], help='L\'algorithme de compression')
    parser.add_argument('input_files', nargs='+', type=str, help='Les fichiers à compresser ou extraire')
    parser.add_argument('--extract', action='store_true', help='Option pour décompresser')

    # Analyse des arguments de la ligne de commande
    args = parser.parse_args()
    output_archive = args.output_archive
    compression_algorithm = args.compression
    input_files = args.input_files

    if args.extract:
        process_files(input_files, output_archive, compression_algorithm, 'extract')
    else:
        process_files(input_files, output_archive, compression_algorithm, 'compress')

if __name__ == "__main__":
    main()
