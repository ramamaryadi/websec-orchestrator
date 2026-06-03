from urllib.parse import urlparse

def get_base_domain(domain):
    parts = domain.split('.')
    if len(parts) >= 3 and domain.endswith(".go.id"):
        return ".".join(parts[-3:])
    if len(parts) >= 2:
        return ".".join(parts[-2:])
    return domain

def is_safe_redirect(original_url, target_url, whitelist):
    try:
        orig_parsed = urlparse(original_url)
        target_parsed = urlparse(target_url)
        
        orig_domain = orig_parsed.netloc.lower()
        target_domain = target_parsed.netloc.lower()
        
        # Strip port numbers if any
        if ":" in orig_domain:
            orig_domain = orig_domain.split(":")[0]
        if ":" in target_domain:
            target_domain = target_domain.split(":")[0]
            
        if not orig_domain or not target_domain:
            return True # Not a valid domain change or local path
            
        if orig_domain == target_domain:
            return True
            
        # Check base domain match
        orig_base = get_base_domain(orig_domain)
        target_base = get_base_domain(target_domain)
        if orig_base == target_base:
            return True
                
        # Check whitelist
        for allowed in whitelist:
            allowed_lower = allowed.lower()
            if target_domain == allowed_lower or target_domain.endswith("." + allowed_lower):
                return True
                
        return False
    except Exception:
        return False
