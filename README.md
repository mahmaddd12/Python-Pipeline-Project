# Python-Pipeline-Project
I was able to run through the first 3 steps, however I kept on getting errors on the SPAdes script due to the the reads not being the same length. I tried to mitigate this by truncating the reads so they could be the same length, but still got the same errors. 

Therefore my wrapper script won't work, and I wasn't able to test if my analyze_contigs script and blast_analysis scripts will work.

The two fastq files I have in the repository are sample data made by taking the 40,000 head of the 2dpi fastq files

My other data folders are in my visual studio the paths are
/home/2025/mahmad12/assembly/spades_output (the spades output from assemble_spades.py)
/home/2025/mahmad12/filtered_data (the filtered data from filter_reads.py)
/home/2025/mahmad12/Python-Pipeline-Project/data (this is the fastq files from the download_sra.py script)

