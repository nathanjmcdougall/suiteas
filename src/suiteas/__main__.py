"""Main module for suiteas package."""
import sys

import suiteas

if len(sys.argv) == 1:
    argv = None
elif len(sys.argv) > 1:
    argv = sys.argv[1:]
else:
    raise AssertionError

suiteas.run_suiteas(argv=argv)
