from papercandy import *
from torch.optim import SGD

from modules import *
from datasets import tfc2016

import time

class MyMonitor(TrainingMonitor):
    def on_updated(self, trainer: Trainer, epoch: int, loss: float, result: ResultCompound):
        if epoch % 100 == 0:
            print(f"Epoch {epoch}: loss {loss * 100}%, {result.input_data.target[0]}->{result.output.max(1, keepdim=True)[1][0].item()}.")

    def on_finished(self, trainer: Trainer, epoch: int):
        trainer.get_network().save(f"models2/{CONFIG().CURRENT.get('group_name', must_exist=True)}_model.pth")
        trainer.get_optimizer().save(f"models2/{CONFIG().CURRENT.get('group_name', must_exist=True)}_optimizer.pth")


def train(batch_size: str, learning_rate: str, batches: str, group_name: str, dataset, my_network: nn.Module = CNN()):
    my_config = new_config("train.cfg")
    my_config.set("batch_size", batch_size)
    my_config.set("learning_rate", learning_rate)
    my_config.set("batches", batches)
    my_config.set("group_name", group_name)
    CONFIG().CURRENT = my_config

    num_batches = my_config.get("batches", must_exist=True, required_type=int)

    my_dataloader = tfc2016.ClassificationDataloader(
        dataset,
        batch_size=my_config.get("batch_size", True, required_type=int),
        num_works=my_config.get("num_works", required_type=int, default_val=1)
    )
    network_container = NetworkC(my_network)
    loss_function_container = LossFunctionC(nn.CrossEntropyLoss())
    optimizer_container = OptimizerC(SGD(
        lr=my_config.get("learning_rate", must_exist=True, required_type=float),
        params=my_network.parameters()
    ))
    my_trainer = Trainer(my_dataloader)
    my_trainer.set_network(network_container)
    my_trainer.set_loss_function(loss_function_container)
    my_trainer.set_optimizer(optimizer_container)
    
    train_start = time.time()
    my_trainer.train(num_batches, monitor=MyMonitor())
    train_stop = time.time()
    # my_trainer = TrainerDataUtils.limit_losses(my_trainer, 0.1)
    print(TrainerDataUtils.analyse(my_trainer))
    gn = CONFIG().CURRENT.get('group_name', must_exist=True)
    draw(my_trainer, 1280, 720).title(gn).save(f"results2/{gn}_loss.png").show()
    print("Trainig Time:", train_stop - train_start)

    my_tester = Tester(my_dataloader)
    my_tester.set_network(network_container)
    test_start = time.time()
    my_tester.test(num_batches)
    test_stop = time.time()
    print("tersting time:", test_stop - test_start)

tasks = [
    [64, 0.1, 2000],
    [64, 0.15, 2000],
    [64, 0.05, 2000],
    [64, 0.5, 2000],
    [64, 0.01, 2000],
    [128, 0.1, 2000],
    [128, 0.15, 2000],
    [128, 0.05, 2000],
    [128, 0.5, 2000],
    [128, 0.01, 2000],
    [32, 0.1, 2000],
    [32, 0.15, 2000],
    [32, 0.05, 2000],
    [32, 0.5, 2000],
    [32, 0.01, 2000],
    [64, 0.1, 8000],
    [64, 0.15, 8000],
    [64, 0.05, 8000],
    [64, 0.5, 8000],
    [64, 0.01, 8000],
    [128, 0.1, 8000],
    [128, 0.15, 8000],
    [128, 0.05, 8000],
    [128, 0.5, 8000],
    [128, 0.01, 8000],
    [32, 0.1, 8000],
    [32, 0.15, 8000],
    [32, 0.05, 8000],
    [32, 0.5, 8000],
    [32, 0.01, 8000],

    [64, 0.1, 2000],
    [64, 0.15, 2000],
    [64, 0.05, 2000],
    [64, 0.5, 2000],
    [64, 0.01, 2000],
    [128, 0.1, 2000],
    [128, 0.15, 2000],
    [128, 0.05, 2000],
    [128, 0.5, 2000],
    [128, 0.01, 2000],
    [32, 0.1, 2000],
    [32, 0.15, 2000],
    [32, 0.05, 2000],
    [32, 0.5, 2000],
    [32, 0.01, 2000],
    [64, 0.1, 8000],
    [64, 0.15, 8000],
    [64, 0.05, 8000],
    [64, 0.5, 8000],
    [64, 0.01, 8000],
    [128, 0.1, 8000],
    [128, 0.15, 8000],
    [128, 0.05, 8000],
    [128, 0.5, 8000],
    [128, 0.01, 8000],
    [32, 0.1, 8000],
    [32, 0.15, 8000],
    [32, 0.05, 8000],
    [32, 0.5, 8000],
    [32, 0.01, 8000],
]
print("Loading dataset")
dataset = tfc2016.TFC2016("data/pcap", 28).shuffle()
print("Dataset loaded")

dataset.get(0).cpu().unpack()[0].shape
i = 0
for task in tasks:
    i += 1
    if 1 <= i < 31:
        train(str(task[0]), str(task[1]), str(task[2]), f"G{i}", dataset)
    elif 31 <= i < 61:
        train(str(task[0]), str(task[1]), str(task[2]), f"G{i}", dataset, LeNet5())
