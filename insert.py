import csv
import time
import argparse

def generate_insert_statement(row, table_name):
    # Generate the column names for the INSERT statement.
    columns = ",".join(row.keys())

    # Generate the values for the INSERT statement.
    values = ",".join(f"'{val}'" for val in row.values())

    # Return the INSERT statement.
    return f"INSERT INTO {table_name} ({columns}) VALUES ({values});\n"

if __name__ == "__main__":
    # Create argument parser to parse the table_name and input_file from the command line
    parser = argparse.ArgumentParser()
    parser.add_argument("table_name", help="Name of the table to insert data into")
    parser.add_argument("input_file", help="Path to the input CSV file")
    args = parser.parse_args()

    start_time = time.time()  # Start the timer

    # Set the output file.
    output_file = "output.txt"

    # Open the input and output files.
    with open(args.input_file, "r", newline="", encoding="utf-8") as csv_input, open(output_file, "w",  encoding="utf-8") as txt_output:
        # Create a CSV reader object.
        csv_reader = csv.DictReader(csv_input, delimiter=";")

        # Loop through the rows of the CSV file and generate the INSERT statements.
        for row in csv_reader:
            insert_statement = generate_insert_statement(row, args.table_name)
            txt_output.write(insert_statement)

    end_time = time.time()  # End the timer
    execution_time = end_time - start_time

    minutes = int(execution_time // 60)
    seconds = int(execution_time % 60)
    milliseconds = int((execution_time - int(execution_time)) * 1000)

    print(f"Execution time: {minutes:02d}:{seconds:02d}.{milliseconds:03d}")
