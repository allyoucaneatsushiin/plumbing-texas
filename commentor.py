import streamlit as st
import csv
import requests
import time
import random
from concurrent.futures import ThreadPoolExecutor, as_completed

# Define websites
websites = [
    {
       
    "WordPress": "Yes",
    "name": "Site 1",
    "url": "https://aereon.com/wp-comments-post.php",
    "referer": "https://aereon.com/ten-things-to-know-for-vapor-recovery-system-selection",
    "origin": "https://aereon.com",
    "comment_post_ID": 2822,
    "csv_file": "comments.csv",
    
},

{
    "WordPress": "Yes",
    "name": "Site 2",
    "url": "https://corover.ai/wp-comments-post.php",
    "referer": "https://corover.ai/safeguarding-digital-lives-decoding-digital-personal-data-protection-act-2023",
    "origin": "https://corover.ai",
    "comment_post_ID": 19364,
    "csv_file": "comments.csv",
    
},

{
    "WordPress": "Yes",
    "name": "Site 3",
    "url": "https://trinityglobalschool.com/wp-comments-post.php",
    "referer": "https://trinityglobalschool.com/class-updates/7th/",
    "origin": "https://trinityglobalschool.com",
    "comment_post_ID": 5393,
    "csv_file": "comments.csv",
    
},

{
    "WordPress": "Yes",
    "name": "Site 4",
    "url": "https://www.fetalmedicineindia.in/wp-comments-post.php",
    "referer": "https://www.fetalmedicineindia.in/dsc_8454/",
    "origin": "https://www.fetalmedicineindia.in",
    "comment_post_ID": 1714,
    "csv_file": "comments.csv",
    
},

{
    "WordPress": "Yes",
    "name": "Site 5",
    "url": "https://www.emiratesscholar.com/wp-comments-post.php",
    "referer": "https://www.emiratesscholar.com/cloud-computing-based-banking-and-management-control/ ",
    "origin": "https://www.emiratesscholar.com",
    "comment_post_ID": 9286,
    "csv_file": "comments.csv",
    
    },
]
import streamlit as st
import csv
import requests
import time
import random
from concurrent.futures import ThreadPoolExecutor, as_completed


# Function to get the public IP of the running machine
def get_public_ip():
    try:
        response = requests.get("https://api64.ipify.org?format=text", timeout=5)
        if response.status_code == 200:
            return response.text
    except:
        return "Unable to fetch IP"


# Display the public IP
public_ip = get_public_ip()
st.write(f"### 🖥️ Running on IP: `{public_ip}`")


# Function to get free proxies
def fetch_free_proxies():
    proxy_sources = [
        "https://www.proxy-list.download/api/v1/get?type=https",
        "https://www.proxyscan.io/download?type=https",
        "https://raw.githubusercontent.com/TheSpeedX/SOCKS-List/master/http.txt",
    ]

    proxies = []
    for url in proxy_sources:
        try:
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                proxy_list = response.text.split("\n")
                proxies.extend(proxy.strip() for proxy in proxy_list if proxy.strip())
        except:
            continue

    return proxies if proxies else None


# Get a list of free proxies
proxies_list = fetch_free_proxies()


# Function to choose a random proxy
def get_random_proxy():
    if proxies_list:
        proxy = random.choice(proxies_list)
        return {"http": f"http://{proxy}", "https": f"https://{proxy}"}
    return None


# Function to build request headers
def build_headers(referer, origin):
    return {
        "User-Agent": random.choice(
            [
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36",
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Safari/605.1.15",
                "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36",
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:91.0) Gecko/20100101 Firefox/91.0",
                "Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1",
            ]
        ),
        "Referer": referer,
        "Origin": origin,
    }


# Function to post comment with proxy
def post_comment_to_site(website, comment, author, email):
    payload = {
        "comment": comment,
        "author": author,
        "email": email,
        "comment_post_ID": website["comment_post_ID"],
        "comment_parent": 0,
    }
    headers = build_headers(website["referer"], website["origin"])

    proxy = get_random_proxy()  # Get a random proxy

    try:
        response = requests.post(
            website["url"], headers=headers, data=payload, timeout=10
        )
        return website["name"], website["url"], response.status_code == 200, response.status_code
    except:
        return website["name"], website["url"], False, 0


# Main function
def main():
    st.title("Automated Comment Poster with Proxies")

    uploaded_file = st.file_uploader("Upload a CSV file with comments", type=["csv"])

    if uploaded_file is not None:
        reader = csv.DictReader(uploaded_file.read().decode("utf-8").splitlines())
        total_comments = sum(1 for _ in reader)
        uploaded_file.seek(0)
        reader = csv.DictReader(uploaded_file.read().decode("utf-8").splitlines())

        success_count, fail_count = 0, 0
        status_placeholder = st.empty()

        for idx, row in enumerate(reader, start=1):
            comment, author, email = row["comment"], row["author"], row["email"]

            with ThreadPoolExecutor(max_workers=len(websites)) as executor:
                futures = {
                    executor.submit(
                        post_comment_to_site, site, comment, author, email
                    ): site
                    for site in websites
                }
                results = []
                for future in as_completed(futures):
                    site_name, site_url, success, code = future.result()
                    results.append((site_name, site_url, success,code))
                    success_count += 1 if success else 0
                    fail_count += 0 if success else 1

                    status_text = "\n".join(
                        [f"{'✅' if s else '❌'} {n} ({u}) ({c})" for n, u, s,c in results]
                    )
                    status_placeholder.markdown(f"### Posting Status:\n{status_text}")

            time.sleep(random.randint(5, 6))

        st.success(
            f"Done! {success_count}/{total_comments * len(websites)} comments posted successfully."
        )
        st.error(f"Failed: {fail_count}/{total_comments * len(websites)}")


if __name__ == "__main__":
    main()
