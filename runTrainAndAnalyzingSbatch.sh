#!/bin/bash

#SBATCH -J dlc-benchmark
#SBATCH -o logs/%x.%j.out
#SBATCH -e logs/%x.%j.err
#SBATCH -D "/users/klavir/${userName}/"
#SBATCH --time=7-00:00:00
#SBACTH -G 1
config_file_name=$1
config_path=$2
service_name_config=$3
video_paths_smb=$4
results_paths_smb=$5
service_name_video_path=$6
service_name_result_path=$7
file_name=$8
current_date=$9
containerName=${10}
userName=${11}
srun --gpus=1 --container-image="${containerName}" --container-mounts="${HOME}:/${userName}" python3 "/${userName}/DeepLabCutWrappers/trainAndAnalyze.py" "${config_path}" "${service_name_config}" "${config_file_name}" "/${userName}" "/${userName}/${file_name}/config.yaml" "${video_paths_smb}" "/${userName}/video_tmp_save_path${current_date}" "${results_paths_smb}" "${service_name_video_path}" "${service_name_result_path}"
rm "${containerName}"
rm -rf "video_tmp_save_path${current_date}"
