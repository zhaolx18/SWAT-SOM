import pandas as pd
import numpy as np
def extract_observed_data(file_path):
    with open(file_path, 'r') as file:
        return [int(line.split()[1]) for line in file.readlines()]
def write_results_to_txt(d1_value, i1_value, output_txt_path):
    with open(output_txt_path, 'w') as file:
        file.write(f"P-FACTOR={d1_value:.2f}\n")
        file.write(f"R-FACTOR={i1_value:.2f}\n")
def process_and_transpose_csv(input_csv_path, output_excel_path, observed_data):

    data = pd.read_csv(input_csv_path, header=None)

    data_cleaned = data.iloc[2:, 1:]
    
    data_transposed = data_cleaned.transpose()
    
    data_numeric = data_transposed.apply(pd.to_numeric, errors='coerce')
    
    data_sorted = data_numeric.apply(lambda x: x.sort_values().values)
    
    data_sorted.insert(0, 'Index', range(1, 1 + len(data_sorted)))
    
    total_count = len(data_sorted)
    data_sorted['Percentage'] = data_sorted['Index'] / total_count * 100
    
    with pd.ExcelWriter(output_excel_path, engine='xlsxwriter') as writer:
        data_sorted.to_excel(writer, sheet_name='Sheet1', index=False, header=False)
    def find_closest_rows(df, target_percentage):
        closest_above = df[df['Percentage'] >= target_percentage].iloc[0]
        closest_below = df[df['Percentage'] <= target_percentage].iloc[-1]
        closest = (closest_above + closest_below) / 2
        return closest
        
    low_percentile_row = find_closest_rows(data_sorted, 2.5)
    high_percentile_row = find_closest_rows(data_sorted, 97.5)

    low_percentile_row = low_percentile_row.drop(['Index', 'Percentage'])
    high_percentile_row = high_percentile_row.drop(['Index', 'Percentage'])
    selected_data = pd.DataFrame([low_percentile_row, high_percentile_row]).transpose()

    with pd.ExcelWriter(output_excel_path, engine='openpyxl', mode='a') as writer:

        if 'Percentiles' not in writer.book.sheetnames:
            selected_data.to_excel(writer, sheet_name='Percentiles', index=False, header=False)
        
        worksheet = writer.sheets['Percentiles']
        for i, value in enumerate(observed_data):
            worksheet.cell(row=i+1, column=3, value=value)
        
 
        total_rows = worksheet.max_row
        count_between = sum(1 for row in range(1, total_rows + 1) 
                            if worksheet.cell(row=row, column=3).value >= worksheet.cell(row=row, column=1).value 
                            and worksheet.cell(row=row, column=3).value <= worksheet.cell(row=row, column=2).value)
        percentage = count_between / total_rows 
        worksheet.cell(row=1, column=4, value=percentage)

        for row in range(1, total_rows + 1):
            a_value = worksheet.cell(row=row, column=1).value  
            b_value = worksheet.cell(row=row, column=2).value  
            worksheet.cell(row=row, column=5, value=b_value - a_value)  


        f1_value = sum(worksheet.cell(row=row, column=5).value for row in range(1, total_rows + 1))
        worksheet.cell(row=1, column=6, value=f1_value)  


        g1_value = f1_value / total_rows
        worksheet.cell(row=1, column=7, value=g1_value)  

        c_values = [worksheet.cell(row=row, column=3).value for row in range(1, total_rows + 1)]
        h1_value = np.std(c_values, ddof=0)  
        worksheet.cell(row=1, column=8, value=h1_value)  

        i1_value = g1_value / h1_value
        worksheet.cell(row=1, column=9, value=i1_value) 
    d1_value = worksheet.cell(row=1, column=4).value
    i1_value = worksheet.cell(row=1, column=9).value
    
    output_txt_path = '95PPU_result.txt'
    write_results_to_txt(d1_value, i1_value, output_txt_path)
        

observed_file_path = ' '  
observed_data = extract_observed_data(observed_file_path)
input_csv_path = ' ' 
output_excel_path = ' ' 
process_and_transpose_csv(input_csv_path, output_excel_path, observed_data)
