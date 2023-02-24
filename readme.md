# Fine-tuning Transformers on Ray Train

This repository contains a modified version of the `run_clm.py` script allowing it to leverage Ray Train for easy HF Accelerate (w/ DeepSpeed) & Transformers fine-tuning in on a distributed Ray cluster.

## Instructions

First, run `bash mount_nvme.sh` to mount the NVMe drives on the GPU nodes in the cluster. This has to be done once.

Next, run `bash example.sh` to fine-tune the `facebook/opt-125m` model on `alllines.txt` (all Shakespeare plays). Models up to `opt-66b` have been tested, but they may require GPU nodes with more RAM for DeepSpeed offload & model saving. The model checkpoints will be uploaded to S3.