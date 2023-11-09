import os
import sys
import time
import zipfile
import deeplabcut
from smb.SMBConnection import SMBConnection

import storeBySmb


def train(project_smb_path, project_smb_service_name, project_zip_file_name, server_prefix, save_dlc_smb_service_name,
          save_dlc_smb_server_path):
    print(save_dlc_smb_service_name)
    print(save_dlc_smb_server_path)
    save_path = save_dlc_smb_server_path + "/" + project_zip_file_name.split(".zip")[0]
    print(save_path)
    conn = SMBConnection('LabRead',
                         'KlavirReadLab20@#',
                         '132.74.242.29',
                         'WORKGROUP',
                         use_ntlm_v2=True)
    assert conn.connect('132.74.242.29', port=445)
    if not os.path.exists(project_smb_path + "/" + project_zip_file_name):
        with open(project_zip_file_name, 'wb') as zip_file:
            conn.retrieveFile(project_smb_service_name, project_smb_path + "/" + project_zip_file_name, zip_file,
                              timeout=60 * 60,
                              show_progress=True)
        time.sleep(5)
        with zipfile.ZipFile(project_zip_file_name, "r") as zip_ref:
            print(project_zip_file_name.split(".zip")[0])
            # if len(zip_ref.infolist()) != 1:
            #     #os.mkdir(server_prefix+"/"+ project_zip_file_name.split(".zip")[0])
            #     zip_ref.extractall(server_prefix + "/"+ project_zip_file_name.split(".zip")[0])
            # else:
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
    conn.close()
    print("Done evaluate, sending...")
    conn = SMBConnection('LabRead',
                         'KlavirReadLab20@#',
                         '132.74.242.29',
                         'WORKGROUP',
                         use_ntlm_v2=True)
    assert conn.connect('132.74.242.29', port=445)
    try:
        print("creating dir: {}".format(save_path))
        conn.createDirectory(save_dlc_smb_service_name, save_path)
    except Exception as e:
        print("error creating dir {} error: {}".format(save_path, e.args))
    try:
        print("sending to: {}".format(save_path))
        storeBySmb.storeDirectory(server_prefix + "/" + project_zip_file_name.split(".zip")[0],
                                  save_path,
                                  save_dlc_smb_service_name)
    except Exception as e:
        print("we got error when sending dlc folder to {}, error:{}".format(save_path, e))
    conn.close()


if __name__ == "__main__":
    train(*sys.argv[1:])
