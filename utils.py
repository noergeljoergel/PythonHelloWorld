import os
import string

def get_root_paths():
    """Wurzelverzeichnisse ermitteln (Windows: Laufwerke, sonst /)."""
    if os.name == "nt":
        roots = []
        for letter in string.ascii_uppercase:
            drive = f"{letter}:\\"
            if os.path.exists(drive):
                roots.append(drive)
        return roots or ["C:\\"]
    else:
        return ["/"]

def list_subdirs(path):
    """Unterordner (ohne Dateien) auflisten, robust gegen Fehler."""
    try:
        return sorted(
            [e.name for e in os.scandir(path) if e.is_dir(follow_symlinks=False)],
            key=lambda s: s.lower()
        )
    except (PermissionError, FileNotFoundError, OSError):
        return []
