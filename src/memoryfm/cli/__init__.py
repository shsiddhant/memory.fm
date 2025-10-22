from platformdirs import user_data_path

base_dir = user_data_path(appname="memoryfm", appauthor=False, ensure_exists=True)
imports_dir = base_dir / "imports"
imports_file = base_dir / "imports.json"
loaded_file = base_dir / "loaded.json"
