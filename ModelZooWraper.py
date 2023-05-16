import os
import sys

import deeplabcut
from smb.SMBConnection import SMBConnection

from storeBySmb import store

video_paths_smb = sys.argv[1]
video_tmp_save_path = sys.argv[2]
results_paths_smb = sys.argv[3]
service_name_video_path = sys.argv[4]
service_name_result_path = sys.argv[5]
superanimal_name = 'superanimal_topviewmouse'

conn = SMBConnection('LabRead',
                     'KlavirReadLab20@#',
                     '132.74.242.29',
                     'WORKGROUP',
                     use_ntlm_v2=True)
assert conn.connect('132.74.242.29', port=445)
# list the files on each share
files = conn.listPath(service_name_video_path, video_paths_smb, timeout=30)
scale_list = range(200, 600, 50)  # image height pixel size range and increment
for file in files:
    if "." != file.filename and ".." != file.filename:
        conn = SMBConnection('LabRead',
                             'KlavirReadLab20@#',
                             '132.74.242.29',
                             'WORKGROUP',
                             use_ntlm_v2=True)
        assert conn.connect('132.74.242.29', port=445)
        tmp_video_path = [os.path.join(video_tmp_save_path, file.filename)]
        with open(tmp_video_path[0], 'wb') as video_file:
            conn.retrieveFile(service_name_video_path, video_paths_smb + "/" + file.filename, video_file,
                              timeout=60 * 60,
                              show_progress=True)
        print("done downloading" + file.filename)
        conn.close()
        deeplabcut.video_inference_superanimal(tmp_video_path, superanimal_name, scale_list=scale_list,videotype=".mpg")

store(video_tmp_save_path, service_name_result_path, results_paths_smb, [".csv", ".h5", "labeled.mp4"], False)
print("done")

