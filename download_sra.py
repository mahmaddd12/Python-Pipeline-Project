import os
import subprocess

# Correct SRR accessions
sra_samples = {
    "Donor1_2dpi": "SRR5660030",
    "Donor1_6dpi": "SRR5660033"
}

# Create output directory
output_dir = "data"
os.makedirs(output_dir, exist_ok=True)

# Function to download and convert SRA to FASTQ
def download_and_convert(sample_name, srx_id):
    print(f"Processing {sample_name} ({srx_id})...")

    # Download .sra file using prefetch if not already downloaded
    sra_path = f"{output_dir}/{srx_id}"
    if not os.path.exists(sra_path):
        prefetch_cmd = f"prefetch {srx_id} -O {output_dir}"
        subprocess.run(prefetch_cmd, shell=True, check=True)

    # Convert to FASTQ and gzip separately
    fastq_dump_cmd = f"fasterq-dump --split-files {srx_id} -O {output_dir} && gzip {output_dir}/{srx_id}_*.fastq"
    subprocess.run(fastq_dump_cmd, shell=True, check=True)

    print(f"Completed: {sample_name}")

# Run for each sample
for sample, srx in sra_samples.items():
    download_and_convert(sample, srx)

print("Download and conversion completed!")
