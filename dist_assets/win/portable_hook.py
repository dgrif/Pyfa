"""Keep portable-build fittings beside the executable, not in an extraction directory."""

import os
import sys
import types

# An explicit save-path option still takes precedence over the portable default.
custom_save_path = any(
    arg.startswith('-s') and not arg.startswith('--') or arg == '--savepath' or arg.startswith('--savepath=')
    for arg in sys.argv[1:])
if not custom_save_path:
    configforced = types.ModuleType('configforced')
    configforced.savePath = os.path.join(os.path.dirname(sys.executable), 'saveddata')
    sys.modules['configforced'] = configforced
