import time
from config import URL_LIST, safe_print
from scanner import scan_website
from report import generate_docx_report

def main():
    safe_print(f"Memuat {len(URL_LIST)} URL dari listsubdomain.txt")
    safe_print("Memulai pemindaian Web Defacement...\n" + "="*40)
    results = []
    for url in URL_LIST:
        result = scan_website(url)
        if result["message"] is not None:
            safe_print(result["message"])
        else:
            safe_print(None)
        results.append(result)
        time.sleep(1) # Jeda 1 detik agar tidak membebani server target (Rate Limiting)
    safe_print("="*40 + "\nPemindaian selesai.")
    
    # Menghasilkan Laporan Word otomatis
    generate_docx_report(results)

if __name__ == "__main__":
    main()