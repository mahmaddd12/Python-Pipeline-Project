import os
import subprocess

# Define directories
output_dir = "filtered_data"
os.makedirs(output_dir, exist_ok=True)  # Ensure the directory exists

# Define samples and their FASTQ files
samples = {
    "Donor1_2dpi": ["data/SRR5660030_1.fastq.gz", "data/SRR5660030_2.fastq.gz"],
    "Donor1_6dpi": ["data/SRR5660033_1.fastq.gz", "data/SRR5660033_2.fastq.gz"]
}

# Define index and reference genome
index_prefix = "HCMV_index"

# Function to run Bowtie2 and filter reads
def filter_reads(sample_name, fastq_files):
    print(f"Processing {sample_name}...")

    # Define file paths
    sam_file = f"{output_dir}/{sample_name}.sam"
    bam_file = f"{output_dir}/{sample_name}.bam"
    filtered_bam = f"{output_dir}/{sample_name}_filtered.bam"

    # Run Bowtie2 alignment
    bowtie_cmd = f"bowtie2 -x {index_prefix} -1 {fastq_files[0]} -2 {fastq_files[1]} -S {sam_file}"
    subprocess.run(bowtie_cmd, shell=True, check=True)

    # Convert SAM to BAM
    subprocess.run(f"samtools view -bS {sam_file} -o {bam_file}", shell=True, check=True)

    # Ensure BAM file exists before filtering
    if not os.path.exists(bam_file):
        print(f"ERROR: BAM file {bam_file} not created! Exiting.")
        exit(1)

    # Filter mapped reads
    subprocess.run(f"samtools view -b -F 4 {bam_file} -o {filtered_bam}", shell=True, check=True)

    # Ensure filtered BAM file exists before proceeding
    if not os.path.exists(filtered_bam):
        print(f"ERROR: Filtered BAM file {filtered_bam} not created! Exiting.")
        exit(1)

    # Count reads before and after filtering
    total_reads = int(subprocess.check_output(f"samtools view -c {bam_file}", shell=True))
    mapped_reads = int(subprocess.check_output(f"samtools view -c {filtered_bam}", shell=True))

    # Log results
    with open("PipelineProject.log", "a") as log_file:
        log_file.write(f"{sample_name} had {total_reads} read pairs before Bowtie2 filtering and {mapped_reads} read pairs after.\n")

    print(f"Filtering complete for {sample_name}")

# Run filtering for each sample
for sample, fastq_files in samples.items():
    filter_reads(sample, fastq_files)

print("Filtering step completed!")
