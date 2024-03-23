iimport subprocess
import os
# Running the base vanilla lottery

script1 = 'Applications/dfs.py'
script2 = 'Applications/file_op_app.py'
script3 = 'MergeSortPar.py'

file = "file_op_2_s_raw_output.txt"
file2 = "file_op_2_s_output.txt"
os.system(f"python3 {script2} -n 2 -f sample_files/s.txt p.txt sample_files/s.txt p2.txt -p_mode 0 > {file}")
os.system(f"python3 eval.py {file}")

file = "file_op_2_s3_raw_output.txt"
file2 = "file_op_2_s3_output.txt"
os.system(f"python3 {script2} -n 2 -f sample_files/s3.txt p.txt sample_files/s3.txt p2.txt -p_mode 0 > {file}")
os.system(f"python3 eval.py {file}")

file = "file_op_4_s3_raw_output.txt"
file2 = "file_op_4_s3_output.txt"
os.system(f"python3 {script2} -n 4 -f sample_files/s.txt p.txt sample_files/s.txt p2.txt sample_files/s3.txt p3.txt sample_files/s3.txt p4.txt -p_mode 0 > {file}")
os.system(f"python3 eval.py {file}")

file = "file_op_8_s3_raw_output.txt"
file2 = "file_op_8_s3_output.txt"
os.system(f"python3 {script2} -n 8 -f sample_files/s.txt p1.txt sample_files/s.txt p2.txt sample_files/s3.txt p3.txt sample_files/s3.txt p4.txt sample_files/s3.txt p5.txt sample_files/s3.txt p6.txt sample_files/s3.txt p7.txt sample_files/s3.txt p8.txt -p_mode 0 > {file}")
os.system(f"python3 eval.py {file}")

# ------------------------------------------------------------------------------------------------

file = "dfs_2_sg_raw_output.txt"
file2 = "dfs_2_sg_output.txt"
os.system(f"python3 {script1} -n 2 -graph graphs/sg.txt -p_mode 0 > {file}")
os.system(f"python3 eval.py {file}")

file = "dfs_2_Wiki-Vote_raw_output.txt"
file2 = "dfs_2_Wiki-Vote_output.txt"
os.system(f"python3 {script1} -n 2 -graph graphs/Wiki-Vote.txt -p_mode 0 > {file}")
os.system(f"python3 eval.py {file}")

file = "dfs_4_Wiki-Vote_raw_output.txt"
file2 = "dfs_4_Wiki-Vote_output.txt"
os.system(f"python3 {script1} -n 4 -graph graphs/Wiki-Vote.txt -p_mode 0 > {file}")
os.system(f"python3 eval.py {file}")

file = "dfs_8_Wiki-Vote_raw_output.txt"
file2 = "dfs_8_Wiki-Vote_output.txt"
os.system(f"python3 {script1} -n 8 -graph graphs/Wiki-Vote.txt -p_mode 0 > {file}")
os.system(f"python3 eval.py {file}")

# ------------------------------------------------------------------------------------------------

file = "merge_sort_2_sample_raw_output.txt"
file2 = "merge_sort_2_sample_output.txt"
os.system(f"python3 {script3} -n 2 -i sample_to_sort.txt -o o.txt -p_mode 0 > {file}")
os.system(f"python3 eval.py {file}")

file = "merge_sort_2_query_numbers_raw_output.txt"
file2 = "merge_sort_2_query_numbers_output.txt"
os.system(f"python3 {script3} -n 2 -i query_numbers.txt -o o.txt -p_mode 0 > {file}")
os.system(f"python3 eval.py {file}")

file = "merge_sort_4_query_numbers_raw_output.txt"
file2 = "merge_sort_4_query_numbers_output.txt"
os.system(f"python3 {script3} -n 4 -i query_numbers.txt -o o.txt -p_mode 0 > {file}")
os.system(f"python3 eval.py {file}")

file = "merge_sort_8_query_numbers_raw_output.txt"
file2 = "merge_sort_8_query_numbers_output.txt"
os.system(f"python3 {script3} -n 8 -i query_numbers.txt -o o.txt -p_mode 0 > {file}")
os.system(f"python3 eval.py {file}")

# ------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------

# Generating data for Alpha inflation protocol here:

file = "file_op_2_s_raw_output.txt"
file2 = "file_op_2_s_output.txt"
os.system(f"python3 {script2} -n 2 -f sample_files/s.txt p.txt sample_files/s.txt p2.txt -p_mode 2 > {file}")
os.system(f"python3 eval.py {file}")

file = "file_op_2_s3_raw_output.txt"
file2 = "file_op_2_s3_output.txt"
os.system(f"python3 {script2} -n 2 -f sample_files/s3.txt p.txt sample_files/s3.txt p2.txt -p_mode 2 > {file}")
os.system(f"python3 eval.py {file}")

file = "file_op_4_s3_raw_output.txt"
file2 = "file_op_4_s3_output.txt"
os.system(f"python3 {script2} -n 4 -f sample_files/s.txt p.txt sample_files/s.txt p2.txt sample_files/s3.txt p3.txt sample_files/s3.txt p4.txt -p_mode 2 > {file}")
os.system(f"python3 eval.py {file}")

file = "file_op_8_s3_raw_output.txt"
file2 = "file_op_8_s3_output.txt"
os.system(f"python3 {script2} -n 8 -f sample_files/s.txt p1.txt sample_files/s.txt p2.txt sample_files/s3.txt p3.txt sample_files/s3.txt p4.txt sample_files/s3.txt p5.txt sample_files/s3.txt p6.txt sample_files/s3.txt p7.txt sample_files/s3.txt p8.txt -p_mode 2 > {file}")
os.system(f"python3 eval.py {file}")

# ------------------------------------------------------------------------------------------------

file = "merge_sort_2_sample_raw_output.txt"
file2 = "merge_sort_2_sample_output.txt"
os.system(f"python3 {script3} -n 2 -i sample_to_sort.txt -o o.txt -p_mode 2 > {file}")
os.system(f"python3 eval.py {file}")

file = "merge_sort_2_query_numbers_raw_output.txt"
file2 = "merge_sort_2_query_numbers_output.txt"
os.system(f"python3 {script3} -n 2 -i query_numbers.txt -o o.txt -p_mode 2 > {file}")
os.system(f"python3 eval.py {file}")

file = "merge_sort_4_query_numbers_raw_output.txt"
file2 = "merge_sort_4_query_numbers_output.txt"
os.system(f"python3 {script3} -n 4 -i query_numbers.txt -o o.txt -p_mode 2 > {file}")
os.system(f"python3 eval.py {file}")

file = "merge_sort_8_query_numbers_raw_output.txt"
file2 = "merge_sort_8_query_numbers_output.txt"
os.system(f"python3 {script3} -n 8 -i query_numbers.txt -o o.txt -p_mode 2 > {file}")
os.system(f"python3 eval.py {file}")

# ------------------------------------------------------------------------------------------------

file = "dfs_2_sg_raw_output.txt"
file2 = "dfs_2_sg_output.txt"
os.system(f"python3 {script1} -n 2 -graph graphs/sg.txt -p_mode 2 > {file}")
os.system(f"python3 eval.py {file}")

file = "dfs_2_Wiki-Vote_raw_output.txt"
file2 = "dfs_2_Wiki-Vote_output.txt"
os.system(f"python3 {script1} -n 2 -graph graphs/Wiki-Vote.txt -p_mode 2 > {file}")
os.system(f"python3 eval.py {file}")

file = "dfs_4_Wiki-Vote_raw_output.txt"
file2 = "dfs_4_Wiki-Vote_output.txt"
os.system(f"python3 {script1} -n 4 -graph graphs/Wiki-Vote.txt -p_mode 2 > {file}")
os.system(f"python3 eval.py {file}")

file = "dfs_8_Wiki-Vote_raw_output.txt"
file2 = "dfs_8_Wiki-Vote_output.txt"
os.system(f"python3 {script1} -n 8 -graph graphs/Wiki-Vote.txt -p_mode 2 > {file}")
os.system(f"python3 eval.py {file}")

# ------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------

# Generating the results for queue protocol here

file = "file_op_2_s_raw_output.txt"
file2 = "file_op_2_s_output.txt"
os.system(f"python3 {script2} -n 2 -f sample_files/s.txt p.txt sample_files/s.txt p2.txt -p_mode 1 > {file}")
os.system(f"python3 eval.py {file}")

file = "file_op_2_s3_raw_output.txt"
file2 = "file_op_2_s3_output.txt"
os.system(f"python3 {script2} -n 2 -f sample_files/s3.txt p.txt sample_files/s3.txt p2.txt -p_mode 1 > {file}")
os.system(f"python3 eval.py {file}")

file = "file_op_4_s3_raw_output.txt"
file2 = "file_op_4_s3_output.txt"
os.system(f"python3 {script2} -n 4 -f sample_files/s.txt p.txt sample_files/s.txt p2.txt sample_files/s3.txt p3.txt sample_files/s3.txt p4.txt -p_mode 1 > {file}")
os.system(f"python3 eval.py {file}")

file = "file_op_8_s3_raw_output.txt"
file2 = "file_op_8_s3_output.txt"
os.system(f"python3 {script2} -n 8 -f sample_files/s.txt p1.txt sample_files/s.txt p2.txt sample_files/s3.txt p3.txt sample_files/s3.txt p4.txt sample_files/s3.txt p5.txt sample_files/s3.txt p6.txt sample_files/s3.txt p7.txt sample_files/s3.txt p8.txt -p_mode 1 > {file}")
os.system(f"python3 eval.py {file}")

# ------------------------------------------------------------------------------------------------

file = "dfs_2_sg_raw_output.txt"
file2 = "dfs_2_sg_output.txt"
os.system(f"python3 {script1} -n 2 -graph graphs/sg.txt -p_mode 1 > {file}")
os.system(f"python3 eval.py {file}")

file = "dfs_2_Wiki-Vote_raw_output.txt"
file2 = "dfs_2_Wiki-Vote_output.txt"
os.system(f"python3 {script1} -n 2 -graph graphs/Wiki-Vote.txt -p_mode 1 > {file}")
os.system(f"python3 eval.py {file}")

file = "dfs_4_Wiki-Vote_raw_output.txt"
file2 = "dfs_4_Wiki-Vote_output.txt"
os.system(f"python3 {script1} -n 4 -graph graphs/Wiki-Vote.txt -p_mode 1 > {file}")
os.system(f"python3 eval.py {file}")

file = "dfs_8_Wiki-Vote_raw_output.txt"
file2 = "dfs_8_Wiki-Vote_output.txt"
os.system(f"python3 {script1} -n 8 -graph graphs/Wiki-Vote.txt -p_mode 1 > {file}")
os.system(f"python3 eval.py {file}")

# ------------------------------------------------------------------------------------------------

file = "merge_sort_2_sample_raw_output.txt"
file2 = "merge_sort_2_sample_output.txt"
os.system(f"python3 {script3} -n 2 -i sample_to_sort.txt -o o.txt -p_mode 1 > {file}")
os.system(f"python3 eval.py {file}")

file = "merge_sort_2_query_numbers_raw_output.txt"
file2 = "merge_sort_2_query_numbers_output.txt"
os.system(f"python3 {script3} -n 2 -i query_numbers.txt -o o.txt -p_mode 1 > {file}")
os.system(f"python3 eval.py {file}")

file = "merge_sort_4_query_numbers_raw_output.txt"
file2 = "merge_sort_4_query_numbers_output.txt"
os.system(f"python3 {script3} -n 4 -i query_numbers.txt -o o.txt -p_mode 1 > {file}")
os.system(f"python3 eval.py {file}")

file = "merge_sort_8_query_numbers_raw_output.txt"
file2 = "merge_sort_8_query_numbers_output.txt"
os.system(f"python3 {script3} -n 8 -i query_numbers.txt -o o.txt -p_mode 1 > {file}")
os.system(f"python3 eval.py {file}")
