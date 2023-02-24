import ray
import ray.util.scheduling_strategies
import subprocess
from pathlib import Path

def force_on_node(node_id: str, remote_func_or_actor_class):
    scheduling_strategy = ray.util.scheduling_strategies.NodeAffinitySchedulingStrategy(
        node_id=node_id, soft=False
    )
    options = {"scheduling_strategy": scheduling_strategy}
    return remote_func_or_actor_class.options(**options)


def run_on_every_node(remote_func_or_actor_class, **remote_kwargs):
    refs = []
    for node in ray.nodes():
        if node["Alive"] and node["Resources"].get("GPU", None):
            refs.append(
                force_on_node(node["NodeID"], remote_func_or_actor_class).remote(**remote_kwargs)
            )
    return ray.get(refs)


@ray.remote(num_gpus=1)
def mount_nvme():
    subprocess.run(
        'drive_name="${1:-/dev/nvme1n1}"; mount_path="${2:-/nvme}"; set -x; sudo file -s "$drive_name"; sudo apt install xfsprogs -y; sudo mkfs -t xfs "$drive_name"; sudo mkdir "$mount_path" && sudo mount "$drive_name" "$mount_path" && sudo chown -R ray "$mount_path"', shell=True, check=True
    )

@ray.remote(num_gpus=1)
def test():
    subprocess.run("mountpoint /nvme", shell=True)

@ray.remote(num_gpus=1)
def prec():
    subprocess.run("ls /nvme", shell=True, check=True)

if __name__ == "__main__":
    ray.init()
    run_on_every_node(mount_nvme)