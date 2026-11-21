#!/bin/bash
cd "$(dirname "$0")" || exit 1
python3 -I jm-copy-groups.py
echo
read -r -p "Press Enter to close"
