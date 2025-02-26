from Bio import SeqIO

# Define paths
contig_file = "assembly/spades_output/contigs.fasta"
log_file_path = "PipelineProject.log"

# Initialize counters
contig_count = 0
total_bp = 0

# Read the contigs file
with open(contig_file, "r") as fasta_file:
    for record in SeqIO.parse(fasta_file, "fasta"):
        if len(record.seq) > 1000:
            contig_count += 1
            total_bp += len(record.seq)

# Log the results
with open(log_file_path, "a") as log_file:
    log_file.write(f"There are {contig_count} contigs > 1000 bp in the assembly.\n")
    log_file.write(f"There are {total_bp} bp in the assembly.\n")

print("Contig analysis completed! Results added to PipelineProject.log.")