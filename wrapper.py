import argparse
import subprocess

# Define script locations
SCRIPTS_DIR = "scripts"
DATA_DIR = "data"
SAMPLE_DIR = "sample_data"
FILTERED_DIR = "filtered_data"
ASSEMBLY_DIR = "assembly"

# Define scripts
SCRIPTS = {
    "filter_reads": f"{SCRIPTS_DIR}/filter_reads.py",
    "assemble_spades": f"{SCRIPTS_DIR}/assemble_spades.py",
    "analyze_contigs": f"{SCRIPTS_DIR}/analyze_contigs.py",
    "blast_analysis": f"{SCRIPTS_DIR}/blast_analysis.py"
}

# Function to run scripts in order
def run_pipeline(data_path):
    print(f"Starting pipeline with data from: {data_path}")

    # Step 2: Filter Reads with Bowtie2
    print("Running Bowtie2 filtering...")
    subprocess.run(f"python {SCRIPTS['filter_reads']} --input {data_path}", shell=True, check=True)

    # Step 3: Assemble with SPAdes
    print("Running SPAdes assembly...")
    subprocess.run(f"python {SCRIPTS['assemble_spades']} --input {FILTERED_DIR}", shell=True, check=True)

    # Step 4: Contig Analysis
    print("Running contig analysis...")
    subprocess.run(f"python {SCRIPTS['analyze_contigs']} --input {ASSEMBLY_DIR}", shell=True, check=True)

    # Step 5: BLAST Analysis
    print("Running BLAST analysis...")
    subprocess.run(f"python {SCRIPTS['blast_analysis']} --input {ASSEMBLY_DIR}", shell=True, check=True)

    print("Pipeline completed! Results are in PipelineProject.log")

# Argument parser for full dataset vs. sample
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run HCMV transcriptome pipeline.")
    parser.add_argument("--sample", action="store_true", help="Run pipeline with sample data.")
    args = parser.parse_args()

    # Choose dataset
    data_path = SAMPLE_DIR if args.sample else DATA_DIR

    # Run the pipeline
    run_pipeline(data_path)