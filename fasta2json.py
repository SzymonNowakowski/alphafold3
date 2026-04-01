import json
import sys
import os
import string

def parse_fasta(fasta_path):
    sequences = []
    current_id = None
    current_seq = []

    if not os.path.exists(fasta_path):
        print(f"Error: {fasta_pathr} does not exist.")
        sys.exit(1)

    with open(fasta_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            if line.startswith(">"):
                if current_id:
                    sequences.append((current_id, "".join(current_seq)))
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
    print(f"Mapping identifiers for: {file_name_no_ext}")

    for index, (original_name, seq_str) in enumerate(fasta_data):
        if index >= len(alphabet):
            print("Error. Too many sequences (limit is letters A-Z).")
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
    print(f"JSON output filename: {output_path}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python fasta2json.py <path_to_FASTA_file> <output_dir>\n\n")
        print("The JSON filename will be the same as for the original FASTA\n")
    else:
        convert_fasta_to_json(sys.argv[1], sys.argv[2])
