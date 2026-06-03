try:
    import docx
    DOCX_AVAILABLE = True
except ImportError:
    DOCX_AVAILABLE = False

if DOCX_AVAILABLE:
    from .generators import generate_docx_report
else:
    from config import safe_print
    def generate_docx_report(results):
        safe_print("\n⚠️  [PERINGATAN] Pustaka 'python-docx' tidak terinstal.")
        safe_print("Silakan instal menggunakan perintah: pip install python-docx")
        safe_print("Laporan Word (.docx) tidak dapat dibuat secara otomatis.\n")
