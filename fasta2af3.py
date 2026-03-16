import json
import sys
import os
import string

def parse_fasta(fasta_path):
    sequences = []
    current_id = None
    current_seq = []

    if not os.path.exists(fasta_path):
        print(f"Błąd: Plik wejściowy {fasta_path} nie istnieje.")
        sys.exit(1)

    with open(fasta_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            if line.startswith(">"):
                if current_id:
                    sequences.append((current_id, "".join(current_seq)))
                # Pobieramy pełny nagłówek dla logów, ale AF3 i tak go nie przyjmie jako ID
                current_id = line[1:].strip()
                current_seq = []
            else:
                current_seq.append(line)
        
        if current_id:
            sequences.append((current_id, "".join(current_seq)))
            
    return sequences

def convert_fasta_to_json(fasta_path, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    base_name = os.path.basename(fasta_path)
    file_name_no_ext = os.path.splitext(base_name)[0]
    
    output_path = os.path.join(output_dir, f"{file_name_no_ext}.json")
    fasta_data = parse_fasta(fasta_path)
    
    # Generator liter alfabetu: A, B, C, D...
    alphabet = string.ascii_uppercase 
    
    af3_json = {
        "name": file_name_no_ext,
        "sequences": [],
        "modelSeeds": [1],
        "dialect": "alphafold3",
        "version": 1
    }

    print("-" * 30)
    print(f"Mapowanie identyfikatorów dla: {file_name_no_ext}")

    for index, (original_name, seq_str) in enumerate(fasta_data):
        if index >= len(alphabet):
            print("Błąd: Zbyt wiele sekwencji (limit AF3 dla id to A-Z).")
            break
            
        letter_id = alphabet[index]
        print(f"  {original_name}  --->  ID: '{letter_id}'")

        af3_json["sequences"].append({
            "protein": {
                "id": letter_id, # Tutaj MUSI być wielka litera
                "sequence": seq_str
            }
        })

    with open(output_path, 'w', encoding='utf-8') as jf:
        json.dump(af3_json, jf, indent=2)
    
    print("-" * 30)
    print(f"Gotowe! Plik JSON: {output_path}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Użycie: python fasta_to_af3_v3.py <sciezka_do_fasta> <katalog_wynikowy>")
    else:
        convert_fasta_to_json(sys.argv[1], sys.argv[2])
