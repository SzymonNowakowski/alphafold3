import json
import os
import sys

def convert_fasta_to_af3_monomers(fasta_path, output_dir):
    """
    Parses a FASTA file and creates individual AlphaFold 3 JSON files 
    for each sequence found (monomer mode).
    """
    # Create the output directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f"Created directory: {output_dir}")

    if not os.path.exists(fasta_path):
        print(f"Error: Input file {fasta_path} not found.")
        sys.exit(1)

    with open(fasta_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Split by '>' and remove empty elements
    entries = content.split('>')
    protein_count = 0

    for entry in entries:
        if not entry.strip():
            continue

        lines = entry.strip().split('\n')
        header = lines[0]
        # Join all subsequent lines to form the full sequence
        sequence = "".join(lines[1:]).strip()

        # Extract ID: look for the string between '|' and '|'
        # Example: >tr|A0A1I0QM73|A0A1I0QM73_9FIRM... -> A0A1I0QM73
        try:
            parts = header.split('|')
            if len(parts) >= 2:
                protein_id = parts[1].strip()
            else:
                # Fallback: take the first word of the header
                protein_id = header.split()[0].strip()
        except Exception as e:
            print(f"Warning: Could not parse header '{header}'. Error: {e}")
            protein_id = "unknown_protein"

        # Construct AlphaFold 3 JSON structure for a monomer
        af3_structure = {
            "name": protein_id,
            "sequences": [
                {
                    "protein": {
                        "id": "A",  # AF3 requires a single uppercase letter for monomers
                        "sequence": sequence
                    }
                }
            ],
            "modelSeeds": [1],
            "dialect": "alphafold3",
            "version": 1
        }

        # Save to individual JSON file
        output_filename = f"{protein_id}.json"
        output_path = os.path.join(output_dir, output_filename)

        with open(output_path, 'w', encoding='utf-8') as json_file:
            json.dump(af3_structure, json_file, indent=2)
        
        print(f"Generated: {output_path}")
        protein_count += 1

    print(f"\nProcessing complete. Total proteins converted: {protein_count}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python fasta2json_monomers.py <input_FASTA> <output_directory>\n\n")
        print("The FASTA contains multiple single chains. The chains will be save to JSON files in output directory with the filename matching the sequence name from FASTA sequence header.\n")
    else:
        convert_fasta_to_af3_monomers(sys.argv[1], sys.argv[2])
