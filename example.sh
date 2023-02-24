#/bin/bash

cp -f alllines.txt /mnt/cluster_storage/alllines.txt
python run_clm_deepspeed_train.py --dataset_name tiny_shakespeare --model_name_or_path facebook/opt-125m --use_slow_tokenizer --output_dir /nvme/out --num_train_epochs 5 --no_keep_linebreaks --learning_rate 5e-4 --weight_decay 0.02 --num_workers 32 --upload_dir "s3://antoni-test/opt_125m_ft"