import requests
import re
import urllib3
import random
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from config import (
    WEBDEFACEMENT_SIGNATURES, 
    CRYPTOJACKING_SIGNATURES, 
    REDIRECT_WHITELIST, 
    INFO_DISCLOSURE_PATHS, 
    USER_AGENTS
)

from .helpers import is_safe_redirect

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def scan_website(url):
    result = {
        "url": url,
        "active": False,
        "status_code": None,
        "defaced": False,
        "keywords_found": [],
        "cryptojacking_detected": False,
        "cryptojacking_signatures": [],
        "redirect_detected": False,
        "redirect_details": [],
        "info_disclosure_detected": False,
        "info_disclosure_details": [],
        "ssl_error": False,
        "ssl_error_details": "",
        "user_agent": "",
        "message": ""
    }
    try:
        # Menggunakan User-Agent acak agar tidak diblokir WAF
        user_agent = random.choice(USER_AGENTS) if USER_AGENTS else 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
        result["user_agent"] = user_agent
        headers = {'User-Agent': user_agent}
        
        # Follow redirects step-by-step with allow_redirects=False to avoid external connection timeouts
        current_url = url
        max_redirects = 10
        redirect_count = 0
        response = None
        verify_ssl = True
        tried_urls = set()
        
        while redirect_count < max_redirects:
            if current_url in tried_urls:
                result["message"] = f"❌ [GAGAL] Terdeteksi loop pengalihan pada {current_url}"
                break
            tried_urls.add(current_url)
            
            try:
                response = requests.get(current_url, headers=headers, timeout=10, allow_redirects=False, verify=verify_ssl)
                result["status_code"] = response.status_code
            except requests.exceptions.SSLError as ssl_err:
                result["ssl_error"] = True
                result["ssl_error_details"] = str(ssl_err)
                if current_url.startswith("https://"):
                    fallback_url = current_url.replace("https://", "http://", 1)
                    try:
                        # Try accessing via http
                        response = requests.get(fallback_url, headers=headers, timeout=10, allow_redirects=False)
                        result["status_code"] = response.status_code
                        current_url = fallback_url
                        verify_ssl = False # disable verification for further redirects
                        continue
                    except requests.exceptions.RequestException as http_err:
                        # Fallback HTTP failed, try HTTPS with verify=False as final recovery
                        try:
                            response = requests.get(current_url, headers=headers, timeout=10, allow_redirects=False, verify=False)
                            result["status_code"] = response.status_code
                            verify_ssl = False
                        except requests.exceptions.RequestException as verify_err:
                            result["message"] = f"❌ [GAGAL] Tidak dapat mengakses {current_url} (SSL Error). Fallback HTTP gagal ({http_err}) dan Bypass SSL gagal ({verify_err})"
                            return result
                else:
                    # Already http, try verify=False in case of proxy issues
                    try:
                        response = requests.get(current_url, headers=headers, timeout=10, allow_redirects=False, verify=False)
                        result["status_code"] = response.status_code
                        verify_ssl = False
                    except requests.exceptions.RequestException as verify_err:
                        result["message"] = f"❌ [GAGAL] Tidak dapat mengakses {current_url} akibat SSL Error: {ssl_err}"
                        return result
            except requests.exceptions.RequestException as e:
                # Catch general connection errors that might wrap SSL errors
                err_str = str(e)
                if "SSLError" in err_str or "ssl" in err_str.lower() or "certificate verify failed" in err_str.lower():
                    result["ssl_error"] = True
                    result["ssl_error_details"] = err_str
                    if current_url.startswith("https://"):
                        fallback_url = current_url.replace("https://", "http://", 1)
                        try:
                            response = requests.get(fallback_url, headers=headers, timeout=10, allow_redirects=False)
                            result["status_code"] = response.status_code
                            current_url = fallback_url
                            verify_ssl = False
                            continue
                        except requests.exceptions.RequestException as http_err:
                            try:
                                response = requests.get(current_url, headers=headers, timeout=10, allow_redirects=False, verify=False)
                                result["status_code"] = response.status_code
                                verify_ssl = False
                            except requests.exceptions.RequestException as verify_err:
                                result["message"] = f"❌ [GAGAL] Tidak dapat mengakses {current_url} (SSL Error). Fallback HTTP gagal ({http_err}) dan Bypass SSL gagal ({verify_err})"
                                return result
                result["message"] = f"❌ [GAGAL] Tidak dapat mengakses {current_url}. Error: {e}"
                return result
                
            if response.status_code in [301, 302, 303, 307, 308]:
                redirect_url = response.headers.get('Location', '')
                if not redirect_url:
                    break
                    
                redirect_url = urljoin(current_url, redirect_url)
                
                # Check if redirect is safe
                if not is_safe_redirect(current_url, redirect_url, REDIRECT_WHITELIST):
                    result["redirect_detected"] = True
                    result["redirect_details"].append(f"HTTP {response.status_code} -> {redirect_url}")
                    result["active"] = True
                    break
                else:
                    result["redirect_details"].append(f"HTTP {response.status_code} -> {redirect_url}")
                    current_url = redirect_url
                    redirect_count += 1
            else:
                break
                
        if response is None:
            result["message"] = f"❌ [GAGAL] Tidak ada respon dari {url}"
            return result
            
        if response.status_code != 200:
            result["active"] = True
            if result["redirect_detected"]:
                result["message"] = f"URL: {url}\n🚨 [BAHAYA] Malicious Redirect terdeteksi! Rincian: {', '.join(result['redirect_details'])}"
            else:
                result["message"] = f"⚠️ [ERROR] URL: {url} mengembalikan status code {response.status_code}"
            return result

        # Analisis Source Code
        result["active"] = True
        soup = BeautifulSoup(response.text, 'html.parser')
        text_content = soup.get_text().lower()
        
        # 2. Deteksi Defacement / SEO Poisoning (Berdasarkan teks terlihat)
        found_keywords = []
        for keyword in WEBDEFACEMENT_SIGNATURES:
            if keyword in text_content:
                found_keywords.append(keyword)
                
        if found_keywords:
            result["defaced"] = True
            result["keywords_found"] = found_keywords

        # 3. Deteksi Cryptojacking (Berdasarkan signature skrip di raw HTML)
        html_content = response.text.lower()
        found_cryptojacking = []
        for sig in CRYPTOJACKING_SIGNATURES:
            if sig.lower() in html_content:
                found_cryptojacking.append(sig)

        if found_cryptojacking:
            result["cryptojacking_detected"] = True
            result["cryptojacking_signatures"] = found_cryptojacking

        # 4. Deteksi Client-side Redirect (Meta Refresh)
        meta_refresh = soup.find('meta', attrs={'http-equiv': lambda x: x and x.lower() == 'refresh'})
        if meta_refresh:
            content = meta_refresh.get('content', '')
            if 'url=' in content.lower():
                try:
                    parts = content.lower().split('url=')
                    if len(parts) > 1:
                        target_url_raw = content[len(parts[0]) + 4:].strip().strip('"').strip("'")
                        target_url = urljoin(url, target_url_raw)
                        if not is_safe_redirect(url, target_url, REDIRECT_WHITELIST):
                            result["redirect_detected"] = True
                            result["redirect_details"].append(f"Meta Refresh -> {target_url}")
                except Exception:
                    pass

        # 5. Deteksi Client-side Redirect (JavaScript window.location / location.replace)
        scripts = soup.find_all('script')
        pattern1 = re.compile(r'(?:window\.)?location(?:\.href)?\s*=\s*[\'"]([^\'"]+)[\'"]')
        pattern2 = re.compile(r'(?:window\.)?location\.replace\(\s*[\'"]([^\'"]+)[\'"]\s*\)')
        
        for script in scripts:
            if script.string:
                script_text = script.string
                matches = pattern1.findall(script_text) + pattern2.findall(script_text)
                for match in matches:
                    target_url = urljoin(url, match)
                    if not is_safe_redirect(url, target_url, REDIRECT_WHITELIST):
                        result["redirect_detected"] = True
                        result["redirect_details"].append(f"JavaScript Redirect -> {target_url}")

        # 6. Deteksi Information Disclosure (Kebocoran Data Sensitif via Path Fuzzing)
        found_leaks = []
        for path, signatures in INFO_DISCLOSURE_PATHS:
            test_url = current_url.rstrip('/') + path
            try:
                # Do not follow redirects to avoid landing on 200 login pages or auth portals
                test_resp = requests.get(test_url, headers=headers, timeout=5, allow_redirects=False, verify=verify_ssl)
                if test_resp.status_code == 200:
                    resp_text = test_resp.text.lower()
                    # Check signatures to verify it is the actual file and not a custom 200 OK error page
                    matches = [sig for sig in signatures if sig.lower() in resp_text]
                    if matches:
                        found_leaks.append(f"{path} (Signatures: {', '.join(matches)})")
            except Exception:
                pass
                
        if found_leaks:
            result["info_disclosure_detected"] = True
            result["info_disclosure_details"] = found_leaks

        # Menyusun Pesan Output
        status_msgs = []
        if result["defaced"]:
            status_msgs.append(f"🚨 [BAHAYA] Defacement/SEO Poisoning terdeteksi! Keywords: {', '.join(found_keywords)}")
        if result["cryptojacking_detected"]:
            status_msgs.append(f"🚨 [BAHAYA] Cryptojacking terdeteksi! Signatures: {', '.join(found_cryptojacking)}")
        if result["redirect_detected"]:
            status_msgs.append(f"🚨 [BAHAYA] Malicious Redirect terdeteksi! Rincian: {', '.join(result['redirect_details'])}")
        if result["info_disclosure_detected"]:
            status_msgs.append(f"🚨 [BAHAYA] Information Disclosure terdeteksi! Jalur bocor: {', '.join(found_leaks)}")
        if result["ssl_error"]:
            status_msgs.append(f"⚠️ [PERINGATAN] Terdeteksi kesalahan sertifikat SSL/TLS pada domain ini ({result['ssl_error_details']})")

        if status_msgs:
            result["message"] = f"URL: {url}\n" + "\n".join(status_msgs)
        else:
            result["message"] = f"✅ [AMAN] {url} bersih dari keyword terlarang, skrip cryptojacking, malicious redirect, dan kebocoran data."

    except requests.exceptions.RequestException as e:
        result["message"] = f"❌ [GAGAL] Tidak dapat mengakses {url}. Error: {e}"
    except Exception as e:
        result["message"] = f"❌ [ERROR] Terjadi kesalahan saat memproses {url}. Error: {e}"
        
    return result
