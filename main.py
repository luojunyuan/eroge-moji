import sys

from moji import moji

import resource

if __name__ == "__main__":
    ret_code = moji()
    resource.qCleanupResources()
    sys.exit(ret_code)
