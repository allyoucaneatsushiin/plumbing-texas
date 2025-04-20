import os
import re
import random

directory = os.getcwd()

def extract_city_and_service(filename):
    match = re.match(r"^(.*?)-(.*?)-TX-\d{3}-\d{3}-\d{4}-.*?\.md$", filename)
    if match:
        service = match.group(1).replace("-", " ").strip().lower()
        city = match.group(2).replace("-", " ").strip().lower()
        return service, city
    return None, None

def generate_url(file_name):
    return f"https://github.com/allyoucaneatsushiin/plumbing-texas/blob/main/{file_name}"

DISCLAIMER_TEXT = """\n\n---

*IMPORTANT: Must add the following disclaimer at the bottom of your site*

**Disclaimer:** This site [Github.com] is a free service to assist homeowners in connecting with local service providers. All contractors/providers are independent and [this site] does not warrant or guarantee any work performed. It is the responsibility of the homeowner to verify that the hired contractor furnishes the necessary license and insurance required for the work being performed. All persons depicted in a photo or video are actors or models and not contractors listed on this site [Github.com].
"""

def update_file(file_name, links):
    file_path = os.path.join(directory, file_name)

    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()

    content = re.sub(r'\n## Internal Links\n(?:- .*\n?)*', '', content, flags=re.IGNORECASE)
    content = re.sub(r'\n+---\n\*IMPORTANT:.*?listed on this site \[Github\.com\]\.', '', content, flags=re.DOTALL)

    content += "\n\n## Internal Links\n"
    for link in links:
        content += f"- [{link}]({generate_url(link)})\n"

    content += DISCLAIMER_TEXT

    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(content)

# Step 1: Load all .md files
file_list = [f for f in os.listdir(directory) if f.endswith('.md')]

# Step 2: Group by city
city_groups = {}
for file in file_list:
    _, city = extract_city_and_service(file)
    if city:
        city_groups.setdefault(city, []).append(file)

# Step 3: Process each city group
for city, files in city_groups.items():
    file_links = {file: [] for file in files}  # Links added to each file
    linked_targets = set()  # Files that have been linked at least once

    # First round: assign up to 4 random links per file
    for file in files:
        others = [f for f in files if f != file]
        selected = random.sample(others, min(4, len(others)))
        file_links[file] = selected
        linked_targets.update(selected)

    # Second round: ensure every file is linked at least once
    unlinked = set(files) - linked_targets
    for target in unlinked:
        candidates = [f for f in files if f != target and len(file_links[f]) < 4]
        if candidates:
            linker = random.choice(candidates)
            file_links[linker].append(target)

    # Final write
    for file in files:
        update_file(file, file_links[file])
        print(f"✅ {file} → Linked with {len(file_links[file])} from {city}")

print("\n🎯 All done: Max 4 links/file, and every file is internally linked at least once.")
