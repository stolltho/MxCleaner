# MxCleaner - Untargeted Metabolomics Data Cleaner

MxCleaner is designed for processing untargeted metabolomics data stored in CSV format. Although initially designed for files exported from Agilent Profinder, it seamlessly accommodates peak area exports from other popular tools such as XCMS and OpenMS. 
The cleaning process, a crucial precursor to subsequent statistical analysis, aims to elevate the quality and reliability of your metabolomics data, ensuring optimal outcomes when utilizing platforms like MetaboAnalyst.

Whether you prefer the interactive environment of a Jupyter Notebook or the streamlined execution of the Python script, MxCleaner provides a versatile solution for refining your metabolomics datasets. Choose the method that aligns with your workflow to unlock the full potential of your untargeted metabolomics data analysis.

## Input
- CSV file (e.g. Agilent Profinder peak area export) 

## Output
- CSV file after applying data cleaning steps specified below

## Data Cleaning Steps based on [Southam et al. 2021](https://pubmed.ncbi.nlm.nih.gov/33236910/):

- Concatenate mass w/ Rt

- Remove QC sample if QC total peak area deviates +/-25% of the median QC total peak area

- Remove features if detected in < 70% of QC samples

- Remove features if absent across all sample groups

- Remove duplicate features if present

- Remove features w/ a QC/Blank ratio < 5

- Remove features if CV > 30% in QC samples

## Header Format of Input File
The input file is expected to have a specific header format:

| Mass | RT   | Blank01 | .. | BlankXX | S01 | .. | SXX | QC01 | .. | QCXX |
|------|------|---------|----|---------|-----|----|-----|------|----|------|
| 101.12 | 0.72 | 2349  |    | 4500    | 398746 |    | 445678 | 500123 |    | 516980 |

- Blank samples should start with "Blank"
- Samples should start with "S", although the flexibility for multiple prefixes exists, such as "S, WT, KO"
- QC samples should start with "QC"
- Delete all other columns

(Note: The order of headers does not matter)

Alternatively, define column header prefixes in either the Jupyter Notebook or as optional arguments in the Python script

## Installation

#### Clone Repository
```bash
git clone https://github.com/stolltho/MxCleaner.git
```
#### Navigate to Repository
```bash
cd repo
```
#### Install Dependencies
```bash
pip install -r requirements.txt
```


## Usage
```bash
python MxCleaner.py example_data/input.csv
````

### Required Argument
- `file_path` : Path to your CSV file (default: example_data/input.csv)

### Optional Arguments

- `--Mass` : Mass column name (default: "Mass")

- `--RT` : RT column name (default: "RT")

- `--Sample` : Sample column prefix (default: "S"), multiple prefixes possible (e.g., "S, WT, KO")

- `--Blank` : Blank column prefix (default: "Blank")

- `--QC` : QC column prefix (default: "QC")

- `--deviation` : Deviation value for QC total peak area (default: 25)

- `--detection_limit` : Detection limit threshold in QC samples (default: 70)

- `--ratio` : QC/Blank ratio threshold (default: 5)

- `--cv` : CV (Coefficient of Variation) threshold in QC samples (default: 30)


## Example Usages
```bash
# Basic usage employing the example data provided
python MxCleaner.py example_data/input.csv

# Custom column names and parameters
python MxCleaner.py example_data/input.csv --Mass "your_mass_column_name" --RT "your_rt_column_name" --Sample "your_sample_column_prefix" --Blank "your_blank_column_prefix" --QC "your_qc_column_prefix" --deviation 25 --detection_limit 70 --ratio 5 --cv 30

# Custom sample names and parameters
python MxCleaner.py example_data/input.csv --ratio 10 --cv 25 --Sample "S, KO"
````

Note: Replace placeholders such as "your_mass_column_name," "your_rt_column_name," etc., with your actual column names.

Feel free to adjust the parameters based on your specific dataset and analysis requirements.

