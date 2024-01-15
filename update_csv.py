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

# Function to generate the UPDATE statement.
def generate_update_statement(row):
    # Get the value of the primary key column(s).
    primary_key_values = {key: row[key] for key in primary_keys.splitlines()}

    # Generate the SET clause of the UPDATE statement.
    set_clause = ",".join(f"{col}='{val}'" for col, val in row.items() if col not in primary_key_values)

    # Generate the WHERE clause of the UPDATE statement.
    where_clause = " AND ".join(f"{col}='{val}'" for col, val in primary_key_values.items())

    # Return the UPDATE statement.
    return f"UPDATE {table_name} SET {set_clause} WHERE {where_clause};\n"

# Open the input and output files.
with open(input_file, "r", newline="",  encoding="utf-8") as csv_input, open(output_file, "w" ,  encoding="utf-8") as txt_output:
    # Create a CSV reader object.
    csv_reader = csv.DictReader(csv_input, delimiter=";")

    # Loop through the rows of the CSV file and generate the UPDATE statements.
    for row in csv_reader:
        update_statement = generate_update_statement(row)
        txt_output.write(update_statement)

end_time = time.time()  # End the timer
execution_time = end_time - start_time

# Convert to minutes and seconds
minutes = int(execution_time // 60)
seconds = int(execution_time % 60)
milliseconds = int((execution_time - int(execution_time)) * 1000)

# Print execution time in minutes, seconds, and milliseconds
print(f"Execution time: {minutes:02d}:{seconds:02d}.{milliseconds:03d}")
