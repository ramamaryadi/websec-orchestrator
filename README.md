# Web Security Orchestrator: Web Defacement & Security Scanner

An automated security scanner and reporting tool designed to monitor the basic security posture and integrity of websites. 

This tool helps cybersecurity operations teams perform routine audits, detect defacements and other anomalies, and generate professional compliance-ready MS Word (`.docx`) reports with remediation steps.

---

## Key Features

- **Web Defacement & SEO Poisoning Detection**: Scan visible page content against a blacklist of keywords associated with online gambling spam and signature defacement markers.
- **Cryptojacking Mitigation**: Detect in-browser cryptocurrency miners by parsing HTML code and analyzing loaded script elements.
- **Malicious Redirect Detection**: Identify traffic hijacking and unauthorized external redirects by tracing HTTP redirect chains, `<meta http-equiv="refresh">` tags, and client-side JavaScript redirections.
- **Information Disclosure Fuzzing**: Probe for sensitive file exposure (e.g., `.env`, `.git/config`, `phpinfo.php`) and validates responses against content signatures to prevent false positives.
- **Resilient SSL/TLS Verification**: Automatically handles certificate errors, with smart fallback to HTTP and bypass verification mechanisms, logging detailed warning logs instead of failing the check.
- **Automated MS Word Report Generator**: Generates clean, well-formatted, corporate-styled DOCX reports containing:
  - An executive summary with tables.
  - A color-coded, sortable status table mapping out clean, vulnerable, and offline subdomains.
  - Dynamic appendices for each vulnerable subdomain, incorporating screenshots and technical details.
  - Category-specific mitigation checklists tailored to the detected vulnerabilities.

---

## Project Architecture

```
Security Orchestrator/
├── checkseopoisoning.py      # Entrypoint script; orchestrates scanning and report generation
├── _verify_urls.py           # Helper script to validate URL loading from targets list
├── listsubdomain.txt         # Plain text list of target URLs to scan (one per line)
├── scanner/                  # Main scanning module
│   ├── __init__.py
│   ├── core.py               # Core scanning logic (HTTP requests, BeautifulSoup parsing, regex)
│   └── helpers.py            # Domain processing and redirect safety validation
├── config/                   # Configuration parameters and whitelists
│   ├── __init__.py
│   ├── signatures.py         # Keyword lists for SEO poisoning and cryptojacking detection
│   ├── whitelist.py          # Trusted external redirection destinations
│   ├── fuzzing.py            # Paths and validation signatures for information disclosure checks
│   ├── user_agents.py        # Random browser User-Agent headers to bypass WAF blocks
│   └── utils.py              # File loading helpers and terminal output unicode fallback printer
└── report/                   # Reporting module
    ├── __init__.py
    ├── constants.py          # Report palette colors, Indonesian month translations, and mitigation lists
    ├── generators.py         # python-docx template layout builder and layout generator
    └── helpers.py            # XML formatting hacks (cell background colors, page numbers, widths)
```

---

## Prerequisites & Installation

### System Requirements
- Python 3.8 or higher installed on your system.

### Install Dependencies
Run the following command in your terminal to install the necessary libraries:
```bash
pip install requests beautifulsoup4 python-docx
```

---

## How to Use

### 1. Configure Target Domains
Edit the [listsubdomain.txt] file in the root directory. Add target URLs, formatted with `http://` or `https://` prefixes, separated by commas or lines:
```text
"https://domain.com",
"https://domain.com",
"https://domain.com"
```

### 2. Execute the Scanner
Start the security orchestration process by running the main entrypoint:
```bash
python checkseopoisoning.py
```

### 3. Retrieve the Report
After completion, the script will output terminal progress and generate a Word document in the root directory named:
`Laporan Hasil Scan Web Defacement - YYYY-MM-DD_HH-MM-SS.docx`

*Note: If the report file is locked or open in another application during execution, a fallback file with a unique timestamp will automatically be generated to prevent data loss.*

---

## Advanced Customization

- **Updating Blacklisted Words**: Modify `config/signatures.py` to add new online slot terms or malicious script signatures.
- **Adjusting Whitelists**: Add partners, CDNs, or external systems to `REDIRECT_WHITELIST` in `config/whitelist.py` to prevent false positive redirect alerts.
- **Extending Sensitive Paths**: Edit `INFO_DISCLOSURE_PATHS` in `config/fuzzing.py` to add custom endpoints or files (e.g., config backups, custom APIs) along with keyword patterns to verify their presence.
- **Modifying Report Aesthetics**: Change the primary/secondary theme colors (`COLOR_PRIMARY_HEX`, etc.) in `report/constants.py` to match your organization's brand identity.
