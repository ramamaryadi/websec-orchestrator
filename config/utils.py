import os

def safe_print(text):
    if text is None:
        print(None)
        return
    try:
        print(text)
    except UnicodeEncodeError:
        replacements = {
            "🚨 ": "",
            "✅ ": "",
            "⚠️ ": "",
            "❌ ": "",
            "🚨": "",
            "✅": "",
            "⚠️": "",
            "❌": "",
            "━": "=",
        }
        clean_text = str(text)
        for emoji, text_rep in replacements.items():
            clean_text = clean_text.replace(emoji, text_rep)
        try:
            print(clean_text)
        except UnicodeEncodeError:
            print(clean_text.encode('ascii', errors='replace').decode('ascii'))

def load_urls(filepath):
    urls = []
    # Since this file resides in config/utils.py, we resolve to its parent directory
    config_dir = os.path.dirname(os.path.abspath(__file__))
    base_dir = os.path.dirname(config_dir)
    full_path = os.path.join(base_dir, filepath)
    if os.path.exists(full_path):
        with open(full_path, "r", encoding="utf-8") as f:
            for line in f:
                url = line.strip().strip('"').strip("'").strip(",").strip('"').strip("'").strip()
                if url.startswith("http"):
                    urls.append(url)
    return urls
    
URL_LIST = load_urls("listsubdomain.txt")
