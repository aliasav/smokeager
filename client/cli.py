#! /usr/bin/env python

"""
smokeager v0.0.1

Usage:
    smokeager inc [n]: increment smoke by [n].
    smokeager status: gives smoking analytics.
    smokeager man: Displays this manual.
    smokeager setup: Setup account for smokeager. Only single account support available presently.
    smokeager clean: destroys current account information.

"""

import sys
import scripts

def entry():        
    scripts.main(sys.argv)

    