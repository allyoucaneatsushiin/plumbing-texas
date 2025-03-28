import streamlit as st
import csv
import requests
import time
import random
from concurrent.futures import ThreadPoolExecutor, as_completed

# Define websites
websites = [
    {
        "name": "Site 1",
        "url": "https://icam-colloquium.ucdavis.edu/wp-comments-post.php",
        "referer": "https://icam-colloquium.ucdavis.edu/2021/05/13/introduction-to-emergence/",
        "origin": "https://icam-colloquium.ucdavis.edu",
        "comment_post_ID": 125,
        "csv_file": "comments.csv",
    },
    {
        "name": "Site 2",
        "url": "https://hukum.upnvj.ac.id/wp-comments-post.php",
        "referer": "https://hukum.upnvj.ac.id/dosen-fakultas-hukum-upn-veteran-jakarta-juga-turut-ikut-menerbitkan-buku/",
        "origin": "https://hukum.upnvj.ac.id",
        "comment_post_ID": 26930,
        "csv_file": "comments.csv",
    },
    {
        "name": "Site 3",
        "url": "https://nanojournal.ifmo.ru/en/wp-comments-post.php",
        "referer": "https://nanojournal.ifmo.ru/en/articles-2/volume3/3-2/chemistry/",
        "origin": "https://nanojournal.ifmo.ru",
        "comment_post_ID": 492,
        "csv_file": "comments.csv",
    },
    {
        "name": "Site 4",
        "url": "https://cssh.uog.edu.et/wp-comments-post.php",
        "referer": "https://cssh.uog.edu.et/lms-wordpress-plugin/",
        "origin": "https://cssh.uog.edu.et",
        "comment_post_ID": 60,
        "csv_file": "comments.csv",
    },
    {
        "name": "Site 5",
        "url": "https://shindig-magazine.com/wp-comments-post.php",
        "referer": "https://shindig-magazine.com/?p=6749",
        "origin": "https://shindig-magazine.com",
        "comment_post_ID": 6749,
        "csv_file": "comments.csv",
    },
    {
        "name": "Site 6",
        "url": "https://vitamagazine.com/wp-comments-post.php",
        "referer": "https://vitamagazine.com/2024/02/01/the-most-flattering-haircut-for-thin-hair-what-to-avoid-heres-what-one-expert-says/",
        "origin": "https://vitamagazine.com",
        "comment_post_ID": 57605,
        "csv_file": "comments.csv",
    },
    {
        "name": "Site 7",
        "url": "https://vitamagazine.com/wp-comments-post.php",
        "referer": "https://vitamagazine.com/2024/02/12/a-brief-history-of-the-crop-top/",
        "origin": "https://vitamagazine.com",
        "comment_post_ID": 58100,
        "csv_file": "comments.csv",
    },
    {
        "name": "Site 8",
        "url": "https://www.mae.gov.bi/wp-comments-post.php",
        "referer": "https://www.mae.gov.bi/2021/10/05/celebration-du-72eme-anniversaire-de-la-fondation-de-la-republique-populaire-de-chine/",
        "origin": "https://www.mae.gov.bi",
        "comment_post_ID": 5286,
        "csv_file": "comments.csv",
    },
    {
        "name": "Site 9",
        "url": "https://blog.bhhscalifornia.com/wp-comments-post.php",
        "referer": "https://blog.bhhscalifornia.com/how-much-does-land-cost-in-california/",
        "origin": "https://blog.bhhscalifornia.com",
        "comment_post_ID": 21898,
        "csv_file": "comments.csv",
    },
    {
        "name": "Site 10",
        "url": "https://pgpaud.unimed.ac.id/wp-comments-post.php",
        "referer": "https://pgpaud.unimed.ac.id/2023/05/27/program-studi-pg-paud-unimed-gelar-webinar-nasional-tentang-peran-ict-dalam-manajemen-lembaga-pendidikan/",
        "origin": "https://pgpaud.unimed.ac.id",
        "comment_post_ID": 3026,
        "csv_file": "comments.csv",
    },
    {
        "name": "Site 12",
        "url": "https://www.pharmachoice.com/wp-comments-post.php",
        "referer": "https://www.pharmachoice.com/flyer/",
        "origin": "https://www.pharmachoice.com",
        "comment_post_ID": 5829,
        "csv_file": "comments.csv",
    },
    {
        "name": "Site 13",
        "url": "https://hukum.upnvj.ac.id/wp-comments-post.php",
        "referer": "https://hukum.upnvj.ac.id/dosen-fakultas-hukum-upn-veteran-jakarta-juga-turut-ikut-menerbitkan-buku/",
        "origin": "https://hukum.upnvj.ac.id",
        "comment_post_ID": 26930,
        "csv_file": "comments.csv",
    },
    {
        "name": "site 14",
        "url": "https://pmsimoesfilhoba.imprensaoficial.org/wp-comments-post.php",
        "referer": "https://pmsimoesfilhoba.imprensaoficial.org/2020/12/28/simoes-filho-boletim-epidemiologico-5/",
        "origin": "https://pmsimoesfilhoba.imprensaoficial.org",
        "comment_post_ID": 12498,
        "csv_file": "comments.csv",
    },
    {
        "name": "site 14",
        "url": "https://www.crimbbd.org/wp-comments-post.php",
        "referer": "https://pmsimoesfilhoba.imprensaoficial.org/2020/12/28/simoes-filho-boletim-epidemiologico-5/",
        "origin": "https://www.crimbbd.org/ijess/5th-issue-vol-3-no-2/",
        "comment_post_ID": 571,
        "csv_file": "comments.csv",
    },
    {
        "name": "Site 15",
        "url": "https://thewayibrew.com/wp-comments-post.php",
        "referer": "https://thewayibrew.com/how-to-brew-your-own-beer/all-grain-brewing/",
        "origin": "https://thewayibrew.com",
        "comment_post_ID": 62,
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
            website["url"], headers=headers, data=payload, proxies=proxy, timeout=10
        )
        return website["name"], website["url"], response.status_code == 200
    except:
        return website["name"], website["url"], False


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
                    site_name, site_url, success = future.result()
                    results.append((site_name, site_url, success))
                    success_count += 1 if success else 0
                    fail_count += 0 if success else 1

                    status_text = "\n".join(
                        [f"{'✅' if s else '❌'} {n} ({u})" for n, u, s in results]
                    )
                    status_placeholder.markdown(f"### Posting Status:\n{status_text}")

            time.sleep(random.randint(5, 6))

        st.success(
            f"Done! {success_count}/{total_comments * len(websites)} comments posted successfully."
        )
        st.error(f"Failed: {fail_count}/{total_comments * len(websites)}")


if __name__ == "__main__":
    main()
