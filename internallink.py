import os
import re
import random

# New standard disclaimer (only once per file)
DISCLAIMER = """\n\n---\n\n*IMPORTANT **Disclaimer:**\n\nThis site [Github.com] is a free service to assist homeowners in connecting with local service providers. All contractors/providers are independent and [Github.com] does not warrant or guarantee any work performed. It is the responsibility of the homeowner to verify that the hired contractor furnishes the necessary license and insurance required for the work being performed. All persons depicted in a photo or video are actors or models and not contractors listed on this site [Github.com].\n\n"""

# Use current directory instead of fixed folder
FOLDER_PATH = os.getcwd()

# Read all Markdown files in the folder
md_files = [f for f in os.listdir(FOLDER_PATH) if f.endswith(".md")]

# Parse metadata from filenames
file_data = []
for filename in md_files:
    parts = filename.replace(".md", "").split("-")
    if len(parts) < 3:
        continue
    service = parts[0]
    city = parts[2]
    file_data.append({
        "filename": filename,
        "service": service,
        "city": city,
        "path": os.path.join(FOLDER_PATH, filename)
    })

# Internal linking logic
for file in file_data:
    same_city_links = [
        f for f in file_data
        if f["city"].lower() == file["city"].lower() and f["filename"] != file["filename"]
    ]

    remaining_needed = 4 - len(same_city_links)

    if remaining_needed > 0:
        same_service_links = [
            f for f in file_data
            if f["service"].lower() == file["service"].lower()
            and f not in same_city_links
            and f["filename"] != file["filename"]
        ]
        random.shuffle(same_service_links)
        same_city_links += same_service_links[:remaining_needed]

    selected_links = same_city_links[:4]

    internal_links_text = "\n\n## Internal Links\n"
    for link in selected_links:
        internal_links_text += f"- [{link['filename']}](https://github.com/allyoucaneatsushiin/plumbing-texas/blob/main/{link['filename']})\n"

    with open(file["path"], "r", encoding="utf-8") as f:
        content = f.read()

    # Remove all previous disclaimers
    content = re.sub(r"\*{1,2}Disclaimer:.*?\*\*[\s\S]*?(?=\n##|\Z)", "", content, flags=re.IGNORECASE)

    # Remove old Internal Links sections
    content = re.sub(r"## Internal Links[\s\S]*", "", content, flags=re.IGNORECASE)

    # Append updated disclaimer and internal links
    content = content.strip() + DISCLAIMER + internal_links_text

    with open(file["path"], "w", encoding="utf-8") as f:
        f.write(content)

print("✅ All files updated with clean disclaimers and internal links.")
