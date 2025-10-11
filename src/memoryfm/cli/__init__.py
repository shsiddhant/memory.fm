# from pathlib import Path
from platformdirs import user_data_path
from memoryfm import __version__

# base_dir = Path.home() / '.local' / 'share' / 'memoryfm'
base_dir = user_data_path(appname="memoryfm", appauthor=False,
                          version=__version__, ensure_exists=True)
imports_dir = base_dir / 'imports'
imports_file = base_dir / 'imports.json'
loaded_file = base_dir / 'loaded.json'

