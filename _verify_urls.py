import os

def load_urls(filepath):
    urls = []
    base_dir = os.path.dirname(os.path.abspath(__file__))
    full_path = os.path.join(base_dir, filepath)
    with open(full_path, "r", encoding="utf-8") as f:
        for line in f:
            url = line.strip().strip('"').strip("'").strip(",").strip('"').strip("'").strip()
            if url.startswith("http"):
                urls.append(url)
    return urls

urls = load_urls("listsubdomain.txt")
print(f"Loaded {len(urls)} URLs")
print("First 3:", urls[:3])
print("Last  3:", urls[-3:])
