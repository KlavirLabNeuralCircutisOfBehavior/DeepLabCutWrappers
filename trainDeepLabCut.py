import os
import sys
import zipfile
import deeplabcut
from smb.SMBConnection import SMBConnection

project_smb_path = sys.argv[1]
project_smb_service_name = sys.argv[2]
project_zip_file_name = sys.argv[3]
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
with zipfile.ZipFile(project_zip_file_name, "r") as zip_ref:
    zip_ref.extractall()
config_path = "/tzuk/" +project_zip_file_name.split(".zip")[0] + "/config.yaml"
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
