import pandas as pd
import numpy as np
import argparse

#----------------------------------------------------------------------------------------

def function(file_path = 'example_data/input.csv',
             Mass   = "Mass",
             RT     = "RT",
             Sample = "S",
             Blank  = "Blank",
             QC     = "QC",
             deviation = 25,
             detection_limit = 70,
             ratio = 5,
             cv = 30):
    
    # Read csv
    df = pd.read_csv(file_path)
    print(f'Shape of original dataset: {df.shape}')

    # Concatenate "Mass" and "RT" to "mass_Rt"
    df['mass_Rt'] = df[Mass].astype(str) + '_' + df[RT].astype(str)

    # Drop "Mass" and "RT"
    df.drop(columns=[Mass, RT], inplace=True)
    

    #--------------------------------------------------------------------------------------
    ### 1. Remove QC sample if QC total peak area deviates +/-25% of the median QC total peak area

    ## Split df in two dfs, a df with and a df w/o 'QC' samples

    # Select columns matching substring 'QC'
    df_qc = df.filter(regex='QC')

    # Filter columns not starting with 'QC'
    df_no_qc = df.loc[:, ~df.columns.str.startswith(QC)]

    # Calculate column sums and percentages
    sum = df_qc.sum()
    pct = sum / sum.median() *100

    # Filter columns based on percentages
    dev = deviation #define deviation in %
    df_qc = df_qc.loc[:, (pct >= (100-dev)) & (pct <= (100+dev))]

    df1 = pd.concat([df_no_qc, df_qc], axis=1)


    #--------------------------------------------------------------------------------------
    ### 2. Remove features if detected in <70% of QC samples

    df2 = df1.copy()

    # Count the number of columns starting with 'QC'
    nqc = np.sum(df2.columns.str.startswith(QC))

    # Subset the DataFrame to remove features detected in <70% of QC samples
    det = 70 #define detection limit in %
    df2 = df2[df2.loc[:, df2.columns.str.startswith(QC)].count(axis=1) > nqc * (det/100)]


    #--------------------------------------------------------------------------------------
    ### 3. Remove features if absent across all sample groups

    df3 = df2.copy()

    # Subset the DataFrame to remove features absent across all sample groups
    df3 = df3[df3[df3.columns[df3.columns.str.startswith(tuple(Sample))]].count(axis=1) > 0]


    #--------------------------------------------------------------------------------------
    ### 4. Remove duplicate features if present

    df4 = df3.copy()

    # Keep only the first occurrence of each value in the specified column
    df4['mass_Rt'] = df4['mass_Rt'].loc[~df4['mass_Rt'].duplicated(keep='first')]


    #--------------------------------------------------------------------------------------
    ### 5. Remove features w/ a QC/Blank ratio <5

    df5 = df4.copy()

    # Calculate mean of QC samples and add in a new column
    df5['QCMean'] = df5.filter(regex='QC').mean(axis=1, skipna=True)

    # Calculate mean of blank samples and add in a new column
    df5['BlankMean'] = df5.filter(regex='Blank').mean(axis=1, skipna=True)

    # Calculate ratio QC/blank
    df5['Ratio'] = df5['QCMean'] / df5['BlankMean']

    # Remove features if ratio < 5, keep rows with NA
    ratio = ratio #define ratio
    df5 = df5[(df5['Ratio'] >= ratio) | df5['Ratio'].isna()]


    #--------------------------------------------------------------------------------------
    ### 6. Remove features if CV >30% in QC samples

    df6 = df5.copy()

    # Get columns matching substring 'QC'
    cols = df6.filter(regex='QC').columns

    # Calculate SD of QC samples and add in a new column
    df6['QC_SD'] = df6[cols].apply(lambda x: np.std(x, ddof=1), axis=1, raw=True)

    # Calculate CV of QC samples and add in a new column
    df6['QC_CV'] = (df6['QC_SD'] / df6['QCMean']) * 100

    # Remove features if CV > 30% in QC samples
    cv = cv #define CV in %
    df6 = df6[df6['QC_CV'] <= cv]


    #--------------------------------------------------------------------------------------
    ### 7. Export cleaned dataset

    df7 = df6.copy()

    # Delete unnecessary columns (matching substring "Blank", "Ratio", "BlankMean", "QCMean", "QC_SD", "QC_CV")
    columns_to_drop = df7.filter(regex='Blank|Ratio|BlankMean|QCMean|QC_SD|QC_CV').columns
    df7 = df7.drop(columns=columns_to_drop)
 
    # Move 'mass_Rt' column to the first position
    df7 = pd.concat([df7['mass_Rt'], df7.drop('mass_Rt', axis=1)], axis=1)

    # Create a new file name with '_cleaned' appended
    cleaned_file_path = file_path.replace('.csv', '_cleaned.csv')

    # Write the cleaned DataFrame to the new CSV file
    df7.to_csv(cleaned_file_path, index=False)
    print(f'Shape of cleaned dataset: {df7.shape}\n')


# -------------------------------------------------------------------------------------------------------------
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Mx Cleaner Script')
                            
    # Required positional argument: file_path
    parser.add_argument('file_path', type=str, help='Path to the input CSV file')

    # Optional arguments with default values
    parser.add_argument('--Mass', type=str, default='Mass', help='Mass column name (default: "Mass")')
    parser.add_argument('--RT', type=str, default='RT', help='RT column name (default: "RT")')
    parser.add_argument('--Sample', type=str, default='S', help='Sample column prefix (default: "S"), multiple prefixes possible e.g. "S, WT, KO"')
    parser.add_argument('--Blank', type=str, default='Blank', help='Blank column prefix (default: "Blank")')
    parser.add_argument('--QC', type=str, default='QC', help='QC column prefix (default: "QC")')
    parser.add_argument('--deviation', type=int, default=25, help='Deviation value (default: 25)')
    parser.add_argument('--detection_limit', type=int, default=70, help='Detection limit value (default: 70)')
    parser.add_argument('--ratio', type=int, default=5, help='Ratio value (default: 5)')
    parser.add_argument('--cv', type=int, default=30, help='CV value (default: 30)')
                                            
    args = parser.parse_args()

    function(args.file_path,
             args.Mass,
             args.RT,
             args.Sample,
             args.Blank,
             args.QC,
             args.deviation,
             args.detection_limit,
             args.ratio,
             args.cv)
    
    # Script logic using the parsed arguments
    print(f'File path: {args.file_path}')
    print(f'Mass column name (default: "Mass"): {args.Mass}')
    print(f'RT column name (default: "RT"): {args.RT}')
    print(f'Sample column prefix (default: "S"): {args.Sample}')
    print(f'Blank column prefix (default: "Blank"): {args.Blank}')
    print(f'QC column prefix (default: "QC"): {args.QC}')
    print(f'%Deviation in QC samples (default: 25): {args.deviation}')
    print(f'%Detected in QC samples (default: 70): {args.detection_limit}')
    print(f'QC/Blank ratio (default: 5): {args.ratio}')
    print(f'%CV in QC samples (default: 30): {args.cv}')

    print('\nDone!')


# python MxCleaner.py example_data/input.csv

# python MxCleaner.py example_data/input.csv --Mass "your_mass_column_name" --RT "your_rt_column_name" --Sample "your_sample_column_prefix"
#  --Blank "your_blank_column_prefix" --QC "your_qc_column_prefix" --deviation 25 --detection_limit 70 --ratio 5 --cv 30

# python MxCleaner.py example_data/input.csv --ratio 10 --cv 25 --Sample "S, KO"
    