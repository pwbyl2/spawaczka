import os
import getpass
import paramiko
import glob
import time
import argparse
import subprocess
from datetime import datetime
current_date = datetime.now().strftime('%Y-%m-%d')
from concurrent.futures import ThreadPoolExecutor, as_completed

script_directory = os.path.dirname(os.path.abspath(__file__))
def connect_to_server(server, password, output_folder, commands):
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        # Connect to server using root user and provided password
        ssh.connect(server['ip'], port=server['port'], username='root', password=password)
        #print(f"Connected to {server['name']}")

        # Save the command outputs to separate files in the 'rob' folder
        for command in commands:
            stdin, stdout, stderr = ssh.exec_command(command)
            exit_status = stdout.channel.recv_exit_status()

            output_text = stdout.read().decode('utf-8')

            filename = f"{output_folder}/{server['name']}_output.txt"
            with open(filename, 'a', encoding='utf-8') as file:

                file.write(output_text)
                #file.write('\n')


        ssh.close()
    except paramiko.AuthenticationException:
        print(f"Failed to connect to {server['name']}. Authentication failed.")
        
        filename = f"{output_folder}/{server['name']}_output.txt"
        with open(filename, 'w', encoding='utf-8') as file:
            file.write("Failed to connect1 to the server.")
            file.write('\n')            
        #print(f"Empty output file created for {server['name']}.")    
            
    except paramiko.SSHException as e:
        print(f"Failed to connect to {server['name']}. SSH error: {str(e)}")
        
        filename = f"{output_folder}/{server['name']}_output.txt"
        with open(filename, 'w', encoding='utf-8') as file:
            file.write("Failed to connect2 to the server.")
            file.write('\n')            
       #print(f"Empty output file created for {server['name']}.")      
            
    except Exception as e:
        print(f"Failed to connect to {server['name']}. Error: {str(e)}")   
        
        # Create empty output file even if connection failed
        filename = f"{output_folder}/{server['name']}_output.txt"
        with open(filename, 'w', encoding='utf-8') as file:
            file.write("Failed to connect3 to the server.")
            file.write('\n')            
        #print(f"Empty output file created for {server['name']}.") 
        


# Create argument parser
parser = argparse.ArgumentParser()
parser.add_argument("--password", help="Password")
parser.add_argument("--settings", help="Path to settings file")
args = parser.parse_args()

# Access the password, settings file, and commands
password = args.password
settings_file = args.settings



commands = [
    "strings /home/postgres/PBSerwis/ProfiBiznesSerwis.exe | grep -E -o '20[0-9]{2}\.[0-9]+\.[0-9]+\.[0-9]+' | head -n 1",
    "strings /home/webservice/public_html/MotoWS/ProfiBiznes.exe | grep -E -o '20[0-9]{2}\.[0-9]+\.[0-9]+\.[0-9]+' | head -n 1",
    "strings /home/webservice/public_html/MotoWS_ZEW/ProfiBiznes.exe | grep -E -o '20[0-9]{2}\.[0-9]+\.[0-9]+\.[0-9]+' | head -n 1",
    "strings /home/samba/Pobieraczka/PobieranieArtykulow.exe | grep -E -o '20[0-9]{2}\.[0-9]+\.[0-9]+\.[0-9]+' | head -n 1",
    "psql -U postgres pgpb -c \"select ver from mbiz.v\$versions order by data_modyfikacji desc limit 1;\" -t -A",
    "psql -U postgres pgpb -c \"select nr_wersji from mbiz.terminal_wersje where zaktualizowano = 'N';\" -t -A"
    
]

## Read server information from settings file
servers = []
if settings_file:
    settings_file_path = os.path.join(script_directory, settings_file)
    with open(settings_file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        for line in lines:
            line = line.strip()
            if line.startswith("name"):
                server = {}
                server['name'] = line.split('=')[1]
            elif line.startswith("ip"):
                server['ip'] = line.split('=')[1]
            elif line.startswith("port"):
                server['port'] = int(line.split('=')[1])
                servers.append(server)


# Execute the commands
for command in commands:
    subprocess.run(command, shell=True)


# Connect to servers and execute commands in parallel
output_folder = 'versions'
os.makedirs(output_folder, exist_ok=True)

start_time = time.time()  # Start the timer

failed_connections = []  # Store the information of servers that failed to connect

with ThreadPoolExecutor(max_workers=20) as executor:
    futures = []
    for server in servers:
        futures.append(executor.submit(connect_to_server, server, password, output_folder, commands))

    # Wait for all tasks to complete
    for future in as_completed(futures):
        try:
            future.result()
        except Exception as e:
            failed_connections.append(future)  # Store the failed connection for later processing
            print(str(e))



# Combine all output files into a single file
combined_filename = f"{output_folder}/{current_date}_all_output_version.txt"
with open(combined_filename, 'w', encoding='utf-8') as combined_file:
    for server in servers:
        filename = f"{output_folder}/{server['name']}_output.txt"
        if os.path.exists(filename):
            combined_file.write(f"{server['name']}\n")
            with open(filename, 'r', encoding='utf-8') as individual_file:
                file_contents = individual_file.read()
                combined_file.write(file_contents)
                combined_file.write('\n')

    #del files
for server in servers:
    file_pattern = os.path.join(output_folder, f"{server['name']}_output.txt")
    files = glob.glob(file_pattern)
    
    for file in files:
        os.remove(file)  


end_time = time.time()  # End the timer
execution_time = end_time - start_time

# Convert to minutes and seconds
minutes = int(execution_time // 60)
seconds = int(execution_time % 60)
milliseconds = int((execution_time - int(execution_time)) * 1000)

# Print execution time in minutes, seconds, and milliseconds
print(f"Execution time: {minutes:02d}:{seconds:02d}.{milliseconds:03d}")






