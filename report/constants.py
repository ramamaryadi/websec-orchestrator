# Color Constants
COLOR_PRIMARY_HEX = "1B365D"       # Navy Blue
COLOR_SECONDARY_HEX = "4A5568"     # Charcoal
COLOR_LIGHT_GRAY_HEX = "F1F5F9"    # Slate Light Gray
COLOR_ALERT_BG_HEX = "FEE2E2"      # Soft Red
COLOR_ALERT_TXT_HEX = "991B1B"     # Dark Red
COLOR_OK_BG_HEX = "DCFCE7"         # Soft Green
COLOR_OK_TXT_HEX = "166534"        # Dark Green
COLOR_INACTIVE_BG_HEX = "F8FAFC"   # Slate Gray BG
COLOR_INACTIVE_TXT_HEX = "64748B"  # Slate Gray TXT

# Translation dict for English to Indonesian months
MONTHS_EN_ID = {
    "January": "Januari", 
    "February": "Februari", 
    "March": "Maret", 
    "April": "April",
    "May": "Mei", 
    "June": "Juni", 
    "July": "Juli", 
    "August": "Agustus",
    "September": "September", 
    "October": "Oktober", 
    "November": "November", 
    "December": "Desember"
}

# Vulnerability Mitigation Recommendations
MITIGATIONS_LIST = [
    ("1. Isolasi dan Pemeliharaan (Maintenance Mode)", 
     "Segera aktifkan mode pemeliharaan pada situs yang terinfeksi untuk membatasi akses publik selama proses pembersihan dilakukan."),
     
    ("2. Pembersihan Source Code dan Database", 
     "Lakukan pemeriksaan pada file index, header, footer, dan database (terutama tabel posts/options) untuk menghapus tautan eksternal judi online (backlink spam) yang disusupkan."),
     
    ("3. Pembersihan Script Cryptominer (Cryptojacking Clean-up)", 
     "Periksa file template tema, widget, dan database terhadap injeksi kode JavaScript bermasalah (seperti coinhive.js, authedmine.js, atau inline script penambang). Hapus seluruh file/skrip mencurigakan tersebut."),

    ("4. Pembersihan Aturan Pengalihan (Redirect Rules Clean-up)", 
     "Periksa berkas konfigurasi .htaccess web server, file konfigurasi Nginx/Apache, atau plugin pengalihan (redirect plugins) CMS untuk menghapus aturan pengalihan mencurigakan ke luar domain."),

    ("5. Sanitasi Script Client-Side (Client-side Redirect Clean-up)", 
     "Hapus tag <meta http-equiv=\"refresh\"> atau kode JavaScript client-side (window.location.href, location.replace) yang mengalihkan ke domain asing dari file sumber tema halaman."),

    ("6. Implementasi Content Security Policy (CSP)", 
     "Konfigurasikan header Content-Security-Policy (CSP) pada web server (seperti Apache/Nginx) untuk membatasi sumber script yang boleh dijalankan (script-src) dan memblokir koneksi WebSocket eksternal yang tidak sah (connect-src)."),

    ("7. Audit Plugin dan CMS (WordPress / Joomla)", 
     "Perbarui CMS ke versi terbaru. Audit seluruh plugin yang terpasang, hapus plugin yang tidak digunakan, dan perbarui seluruh plugin aktif ke versi terbaru untuk menutup celah eksploitasi."),
      
    ("8. Investigasi Log Akses (Forensik Log)", 
     "Analisis access log dan error log web server untuk mengidentifikasi alamat IP penyerang, waktu eksploitasi, serta file atau plugin rentan yang dieksploitasi."),
      
    ("9. Implementasi Web Application Firewall (WAF)", 
     "Gunakan WAF (seperti Cloudflare atau ModSecurity) untuk mendeteksi dan memblokir lalu lintas mencurigakan, serangan injeksi SQL, cross-site scripting (XSS), serta aktivitas pemindaian otomatis."),
      
    ("10. Pemantauan SEO & Keamanan Berkala", 
     "Daftarkan seluruh situs di Google Search Console untuk menerima notifikasi masalah keamanan secara real-time dan ajukan peninjauan kembali (request review) setelah situs dibersihkan."),

    ("11. Penonaktifan Akses Berkas Sensitif (Directory Access Control)", 
     "Segera konfigurasikan file `.htaccess` (Apache) atau konfigurasi blok server (Nginx) untuk menolak akses publik (kembalikan status 403 Forbidden) ke direktori rahasia seperti `.git/config` atau file konfigurasi `.env`. Batasi juga akses eksternal ke file `phpinfo.php` hanya untuk IP administrator internal."),
      
    ("12. Rotasi Kredensial (Credential Rotation)", 
     "Jika berkas `.env` sempat terakses secara publik, segera ganti password database, kunci enkripsi aplikasi, token API, dan kredensial eksternal lainnya yang didefinisikan dalam berkas tersebut untuk menghindari eksploitasi susulan."),
      
    ("13. Pembaruan dan Pemulihan Konfigurasi Sertifikat SSL/TLS", 
     "Segera perbarui atau instal ulang sertifikat SSL/TLS yang valid dan tepercaya (seperti menggunakan Let's Encrypt). Pastikan sertifikat tersebut dikonfigurasi dengan benar untuk mencakup nama domain dan semua URL (misalnya dengan sertifikat wildcard atau menentukan Subject Alternative Names (SAN) yang cocok) guna mengatasi kesalahan Hostname Mismatch.")
]
