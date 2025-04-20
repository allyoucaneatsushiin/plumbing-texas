import os
import re
import random

# Define the directory containing the .md files (current directory where the script is run)
directory = os.getcwd()  # This gets the current working directory

# Function to extract city and service from the filename
def extract_city_and_service(filename):
    match = re.match(r"^(.*?)-(.*?)-TX-\d{3}-\d{3}-\d{4}-.*?\.md$", filename)
    if match:
        service = match.group(1).replace("-", " ").strip()
        city = match.group(2).replace("-", " ").strip()
        return service, city
    return None, None

# Scan the directory for all .md files
file_list = [f for f in os.listdir(directory) if f.endswith('.md')]

# Group files by city and service
city_groups = {}
service_groups = {}

for file in file_list:
    service, city = extract_city_and_service(file)
    if service and city:
        if city not in city_groups:
            city_groups[city] = []
        if service not in service_groups:
            service_groups[service] = []
        city_groups[city].append(file)
        service_groups[service].append(file)

# Function to generate the URL for each file
def generate_url(file_name):
    return f"https://github.com/allyoucaneatsushiin/plumbing-texas/blob/main/{file_name}"

# Function to add internal links to a file
def add_internal_links(file_name, links):
    file_path = os.path.join(directory, file_name)
    with open(file_path, 'a') as file:
        file.write("\n\n## Internal Links\n")
        for link in links:
            file.write(f"- [{link}]({generate_url(link)})\n")

# Process each file to add internal links
for file in file_list:
    service, city = extract_city_and_service(file)
    if service and city:
        # Gather related files from the same city or service
        related_files = []

        # First, try to get files from the same city
        same_city_files = [f for f in city_groups[city] if f != file]
        related_files.extend(same_city_files)

        # If less than 3 links, add files from the same service
        if len(related_files) < 3:
            same_service_files = [f for f in service_groups[service] if f != file]
            related_files.extend(same_service_files)

        # Ensure there are 3-4 internal links
        selected_links = random.sample(related_files, min(4, len(related_files)))
        
        # Add the internal links to the file
        add_internal_links(file, selected_links)

print("Internal linking completed for all files in the folder.")
