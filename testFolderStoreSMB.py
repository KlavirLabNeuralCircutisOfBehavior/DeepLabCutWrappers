import sys

import storeBySmb

folder_path = sys.argv[1]
print(folder_path)
storeBySmb.storeDirectory(folder_path,"/tzuk_test","deepLabCutFiles")