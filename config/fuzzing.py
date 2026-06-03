# Modul Path Fuzzing untuk deteksi kebocoran data sensitif (Information Disclosure)
# Format: (path, list_of_signatures)
INFO_DISCLOSURE_PATHS = [
    ("/.git/config", ["[core]", "repositoryformatversion"]),
    ("/.git/HEAD", ["ref: refs/heads/"]),
    ("/.env", ["DB_", "APP_ENV", "APP_KEY", "MAIL_"]),
    ("/phpinfo.php", ["phpinfo()", "php version", "system ", "build date"]),
    ("/wp-config.php.bak", ["DB_NAME", "DB_USER", "DB_PASSWORD", "wp-config"]),
    ("/database.sql", ["CREATE TABLE", "INSERT INTO", "MySQL dump"]),
    ("/db.sql", ["CREATE TABLE", "INSERT INTO", "MySQL dump"]),
    ("/backup.sql", ["CREATE TABLE", "INSERT INTO", "MySQL dump"]),
    ("/composer.json", ["\"require\"", "\"dependencies\"", "\"name\""]),
    ("/package.json", ["\"dependencies\"", "\"devDependencies\"", "\"name\""])
]
