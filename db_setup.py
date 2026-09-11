#!/usr/bin/env python
"""Initialize database (legacy command name).

Deprecated: prefer `python init_db.py` or `python init_db.py --reset`.
Kept as a thin wrapper so existing muscle memory / docs keep working.
"""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import init_db  # noqa: E402

if __name__ == '__main__':
    init_db.main()
