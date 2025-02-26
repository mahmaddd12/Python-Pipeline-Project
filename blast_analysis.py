import os
import subprocess
from Bio import SeqIO

# Define paths
contig_file = "assembly/spades_output/contigs.fasta"
longest_contig_file = "assembly/longest_contig.fasta"
blast_db = "Betaherpes_DB"
blast_output = "assembly/blast_results.txt"
log_file_path = "PipelineProject.log"

# Step 1: Find the longest contig
longest_contig = None
max_length = 0

with open(contig_file, "r") as fasta_file:
    for record in SeqIO.parse(fasta_file, "fasta"):
        if len(record.seq) > max_length:
            longest_contig = record
            max_length = len(record.seq)

# Save longest contig to a separate file
if longest_contig:
    with open(longest_contig_file, "w") as out_fasta:
        SeqIO.write(longest_contig, out_fasta, "fasta")

# Step 2: Create a local BLAST database for Betaherpesvirinae (if not already created)
if not os.path.exists(blast_db):
    print("Creating BLAST database...")
    subprocess.run(f"makeblastdb -in {contig_file} -dbtype nucl -out {blast_db}", shell=True, check=True)

# Step 3: Run BLAST
print("Running BLAST search...")
blast_cmd = f"blastn -query {longest_contig_file} -db {blast_db} -out {blast_output} -max_target_seqs 10 -outfmt '6 sacc pident length qstart qend sstart send bitscore evalue stitle'"
subprocess.run(blast_cmd, shell=True, check=True)

# Step 4: Log BLAST results
with open(blast_output, "r") as blast_results, open(log_file_path, "a") as log_file:
    log_file.write("sacc\tpident\tlength\tqstart\tqend\tsstart\tsend\tbitscore\tevalue\tstitle\n")
    for line in blast_results:
        log_file.write(line)

print("BLAST analysis completed! Results added to PipelineProject.log.")