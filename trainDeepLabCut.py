import sys

import deeplabcut

config_path = sys.argv[1]
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
