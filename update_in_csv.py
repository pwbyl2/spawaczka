import csv
import time
import sys

# Get the table name and primary keys from command-line arguments
if len(sys.argv) < 4:
    print("Error: Table name and primary keys must be provided as command-line arguments.")
    sys.exit(1)

table_name = sys.argv[1]
primary_keys = sys.argv[2]
input_file = sys.argv[3]

start_time = time.time()  # Start the timer

# Set the input and output files.
output_file = "output.txt"

# Open the input and output files.
with open(input_file, "r", newline="", encoding="utf-8") as csv_input, open(output_file, "w",  encoding="utf-8") as txt_output:
    # Create a CSV reader object.
    csv_reader = csv.DictReader(csv_input, delimiter=";")

    # Read all rows from the CSV file and group them by primary key values.
    rows_grouped = {}
    for row in csv_reader:
        key = tuple(row[key] for key in primary_keys.splitlines())
        rows_grouped.setdefault(key, []).append(row)

    # Generate the SET clause of the UPDATE statement.
    set_clause = ", ".join(f"{col}='{val}'" for col, val in rows_grouped[list(rows_grouped.keys())[0]][0].items() if col not in primary_keys.splitlines())

    # Generate the IN clause of the UPDATE statement with all primary key values.
    in_values = ", ".join(f"'{tuple(row[pk] for pk in primary_keys.splitlines())[0]}'" for row_group in rows_grouped.values() for row in row_group)

    # Write the single UPDATE statement to the output file.
    txt_output.write(f"UPDATE {table_name} SET {set_clause} WHERE ({primary_keys}) IN ({in_values});\n")

end_time = time.time()  # End the timer
execution_time = end_time - start_time

# Convert to minutes and seconds
minutes = int(execution_time // 60)
seconds = int(execution_time % 60)
milliseconds = int((execution_time - int(execution_time)) * 1000)

# Print execution time in minutes, seconds, and milliseconds
print(f"Execution time: {minutes:02d}:{seconds:02d}.{milliseconds:03d}")
