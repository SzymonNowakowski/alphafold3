import json
import os
import sys

def convert_fasta_to_af3_monomers(fasta_path, output_dir):
    """
    Parses a FASTA file and creates individual AlphaFold 3 JSON files 
    for each sequence found. If more than 100 files are generated, 
    they are saved in subdirectories (0, 1, 2...) in batches of 100.
    """
    if not os.path.exists(fasta_path):
        print(f"Error: Input file {fasta_path} not found.")
        sys.exit(1)

    with open(fasta_path, 'r', encoding='utf-8') as f:
        content = f.read()

    entries = [e for e in content.split('>') if e.strip()]
    protein_count = 0

    for entry in entries:
        lines = entry.strip().split('\n')
        header = lines[0]
        sequence = "".join(lines[1:]).strip()

        try:
            parts = header.split('|')
            protein_id = parts[1].strip() if len(parts) >= 2 else header.split()[0].strip()
        except Exception as e:
            print(f"Warning: Could not parse header '{header}'. Error: {e}")
            protein_id = "unknown_protein"

        af3_structure = {
            "name": protein_id,
            "sequences": [
                {
                    "protein": {
                        "id": "A",
                        "sequence": sequence
                    }
                }
            ],
            "modelSeeds": [1],
            "dialect": "alphafold3",
            "version": 1
        }

        # Batching logic: determine subdirectory if total entries > 100
        current_dest_dir = output_dir
        if len(entries) > 100:
            batch_num = str(protein_count // 100)
            current_dest_dir = os.path.join(output_dir, batch_num)

        if not os.path.exists(current_dest_dir):
            os.makedirs(current_dest_dir)

        output_path = os.path.join(current_dest_dir, f"{protein_id}.json")

        with open(output_path, 'w', encoding='utf-8') as json_file:
            json.dump(af3_structure, json_file, indent=2)
        
        protein_count += 1

    print(f"\nProcessing complete. Total proteins converted: {protein_count}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python fasta2json_monomers.py <input_FASTA> <output_directory>\n")
        print("The FASTA contains multiple single chains. The chains will be saved to JSON files.")
        print("If more than 100 sequences exist, they will be organized into subdirectories (0, 1, 2...) in batches of 100.\n")
    else:
        convert_fasta_to_af3_monomers(sys.argv[1], sys.argv[2])
