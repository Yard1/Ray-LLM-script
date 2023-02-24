# Fine-tuning Transformers on Ray Train

This repository contains a modified version of the [`deepspeed_with_config_support.py` script](https://github.com/huggingface/accelerate/blob/main/examples/by_feature/deepspeed_with_config_support.py) allowing it to leverage Ray Train for easy HF Accelerate w/ DeepSpeed Transformers fine-tuning in on a distributed Ray cluster.

## Instructions

First, run `bash mount_nvme.sh` to mount the NVMe drives on the GPU nodes in the cluster. This has to be done once.

Next, run `bash example.sh` to fine-tune the `facebook/opt-125m` model on `alllines.txt` (all Shakespeare plays). Models up to `opt-66b` have been tested, but they may require GPU nodes with more RAM for DeepSpeed offload & model saving and/or lower batch size to avoid CUDA OOMs. The model checkpoints will be uploaded to S3.

WARNING: Ray Train checkpointing will cause OOMs with very large checkpoints (from models with >20b parameters). We are working on a fix but for now make sure that no checkpoint is reported in `session.report`. Furthermore, DeepSpeed will require a substantial amount of RAM to save the final checkpoint, as it will gather weights from all partitions onto one node. It is recommended to use large instances, eg. g5.48xlarge when training with `opt-66b` or similar.