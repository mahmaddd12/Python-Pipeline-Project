import os
import subprocess

# Define paths
filtered_dir = "filtered_data"
assembly_dir = "assembly"
spades_output = f"{assembly_dir}/spades_output"

# Sample names and their filtered BAM files
samples = {
    "Donor1_2dpi": f"{filtered_dir}/Donor1_2dpi_filtered.bam",
    "Donor1_6dpi": f"{filtered_dir}/Donor1_6dpi_filtered.bam"
}

# Create assembly output directory
os.makedirs(spades_output, exist_ok=True)

# Convert BAM to FASTQ for SPAdes
for sample, bam_file in samples.items():
    print(f"Converting {sample} BAM to FASTQ...")
    
    # Generate paired-end FASTQ files
    fastq_r1 = f"{assembly_dir}/{sample}_R1.fastq"
    fastq_r2 = f"{assembly_dir}/{sample}_R2.fastq"
    
    # Convert BAM to paired-end FASTQ
    bam_to_fastq_cmd = f"samtools fastq -1 {fastq_r1} -2 {fastq_r2} {bam_file}"
    subprocess.run(bam_to_fastq_cmd, shell=True, check=True)

    # Step 1: Check line counts and truncate R1 to match R2
    r1_line_count = int(subprocess.check_output(f"wc -l {fastq_r1}", shell=True).split()[0])
    r2_line_count = int(subprocess.check_output(f"wc -l {fastq_r2}", shell=True).split()[0])
    
    if r1_line_count != r2_line_count:
        # Truncate R1 to match the length of R2
        truncated_r1 = f"{assembly_dir}/{sample}_R1_truncated.fastq"
        subprocess.run(f"head -n {r2_line_count} {fastq_r1} > {truncated_r1}", shell=True, check=True)
        fastq_r1 = truncated_r1  # Use the truncated R1 file
        print(f"Truncated {fastq_r1} to match R2")

# Run SPAdes Assembly
print("Running SPAdes assembly...")

spades_cmd = f"spades.py -k 99 --only-assembler --pe1-1 {assembly_dir}/Donor1_2dpi_R1.fastq --pe1-2 {assembly_dir}/Donor1_2dpi_R2.fastq --pe2-1 {assembly_dir}/Donor1_6dpi_R1.fastq --pe2-2 {assembly_dir}/Donor1_6dpi_R2.fastq -o {spades_output}"
subprocess.run(spades_cmd, shell=True, check=True)

# Log the command used
with open("PipelineProject.log", "a") as log_file:
    log_file.write(f"SPAdes command used: {spades_cmd}\n")

print("Assembly completed! Results are in the 'assembly/spades_output' directory.")