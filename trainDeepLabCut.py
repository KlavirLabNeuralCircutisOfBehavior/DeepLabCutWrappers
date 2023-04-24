import os
import sys
import time
import zipfile
import deeplabcut
from smb.SMBConnection import SMBConnection

project_smb_path = sys.argv[1]
project_smb_service_name = sys.argv[2]
project_zip_file_name = sys.argv[3]
server_prefix = sys.argv[4]
conn = SMBConnection('LabRead',
                     'KlavirReadLab20@#',
                     '132.74.242.29',
                     'WORKGROUP',
                     use_ntlm_v2=True)
assert conn.connect('132.74.242.29', port=445)
with open(project_zip_file_name, 'wb') as zip_file:
    conn.retrieveFile(project_smb_service_name, project_smb_path + "/" + project_zip_file_name, zip_file,
                      timeout=60 * 60,
                      show_progress=True)
time.sleep(5)
with zipfile.ZipFile(project_zip_file_name, "r") as zip_ref:
    if len(zip_ref.infolist()) != 1:
        os.mkdir(server_prefix+"/"+ project_zip_file_name.split(".zip")[0])
        zip_ref.extractall(server_prefix + "/"+ project_zip_file_name.split(".zip")[0])
    else:
        zip_ref.extractall(server_prefix + "/")

time.sleep(5)
config_path = server_prefix + "/" + project_zip_file_name.split(".zip")[0] + "/config.yaml"
print(config_path)
deeplabcut.create_training_dataset(
    config_path,
    num_shuffles=3,
    net_type="resnet_50",
    # crop_sampling="density"
)

deeplabcut.train_network(
    config_path,
    saveiters=10000,
    maxiters=100000,
    allow_growth=True,
)
print("Done training")
deeplabcut.evaluate_network(
    config_path,
    plotting=False,
)
print("Done evaluate")
