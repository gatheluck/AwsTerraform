import argparse
import logging
import os
import pathlib
from typing import Final

import torch
import torch.distributed as dist
import torch.nn as nn
import torch.nn.functional as F
import torch.nn.parallel
import torch.optim
import torch.utils.data
import torch.utils.data.distributed
import torchvision
import torchvision.models
import torchvision.transforms as transforms

logger: Final = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

classes: Final = (
    "plane",
    "car",
    "bird",
    "cat",
    "deer",
    "dog",
    "frog",
    "horse",
    "ship",
    "truck",
)


# https://github.com/pytorch/tutorials/blob/master/beginner_source/blitz/cifar10_tutorial.py#L118
class Net(nn.Module):
    def __init__(self) -> None:
        super(Net, self).__init__()
        self.conv1: Final = nn.Conv2d(3, 6, 5)
        self.pool: Final = nn.MaxPool2d(2, 2)
        self.conv2: Final = nn.Conv2d(6, 16, 5)
        self.fc1: Final = nn.Linear(16 * 5 * 5, 120)
        self.fc2: Final = nn.Linear(120, 84)
        self.fc3: Final = nn.Linear(84, 10)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        x = self.pool(F.relu(self.conv1(x)))
        x = self.pool(F.relu(self.conv2(x)))
        x = x.view(-1, 16 * 5 * 5)
        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))
        x = self.fc3(x)
        return x


def _train(args):
    is_distributed: Final = len(args.hosts) > 1 and args.dist_backend is not None
    logger.debug("Distributed training - {}".format(is_distributed))

    if is_distributed:
        # Initialize the distributed environment.
        world_size: Final = len(args.hosts)
        os.environ["WORLD_SIZE"] = str(world_size)
        host_rank: Final = args.hosts.index(args.current_host)
        os.environ["RANK"] = str(host_rank)
        dist.init_process_group(
            backend=args.dist_backend, rank=host_rank, world_size=world_size
        )
        logger.info(
            "Initialized the distributed environment: '{}' backend on {} nodes. ".format(
                args.dist_backend, dist.get_world_size()
            )
            + "Current host rank is {}. Using cuda: {}. Number of gpus: {}".format(
                dist.get_rank(), torch.cuda.is_available(), args.num_gpus
            )
        )

    device: Final = "cuda" if torch.cuda.is_available() else "cpu"
    logger.info("Device Type: {}".format(device))

    logger.info("Loading Cifar10 dataset")
    transform: Final = transforms.Compose(
        [transforms.ToTensor(), transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))]
    )

    trainset: Final = torchvision.datasets.CIFAR10(
        root=args.data_dir, train=True, download=True, transform=transform
    )
    train_loader = torch.utils.data.DataLoader(
        trainset, batch_size=args.batch_size, shuffle=True, num_workers=args.workers
    )

    logger.info("Model loaded")
    model = Net()

    if torch.cuda.device_count() > 1:
        logger.info("Gpu count: {}".format(torch.cuda.device_count()))
        model = nn.DataParallel(model)

    model = model.to(device)

    criterion = nn.CrossEntropyLoss().to(device)
    optimizer = torch.optim.SGD(model.parameters(), lr=args.lr, momentum=args.momentum)

    for epoch in range(0, args.epochs):
        running_loss = 0.0
        for i, data in enumerate(train_loader):
            # get the inputs
            inputs, labels = data
            inputs, labels = inputs.to(device), labels.to(device)

            # zero the parameter gradients
            optimizer.zero_grad()

            # forward + backward + optimize
            outputs = model(inputs)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()

            # print statistics
            running_loss += loss.item()
            if i % 2000 == 1999:  # print every 2000 mini-batches
                print("[%d, %5d] loss: %.3f" % (epoch + 1, i + 1, running_loss / 2000))
                running_loss = 0.0
    print("Finished Training")
    return _save_model(model, pathlib.Path(args.model_dir))


def _save_model(
    model: nn.Module, save_dir: pathlib.Path, filename: str = "model.pth"
) -> None:
    """Save model weight under spacified directory.

    Args:
        model (torch.nn.Module): A pytorch model.
        save_dir (pathlib.Path): A path where the model weight is saved.

    Note:
        Model weight is saved as recommended way as follows.
        http://pytorch.org/docs/master/notes/serialization.html
    """
    save_dir.mkdir(exist_ok=True, parents=True)
    save_path: Final = save_dir / filename
    logger.info("Saving the model to `%s`.", str(save_path))
    torch.save(model.cpu().state_dict(), save_path)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--workers",
        type=int,
        default=2,
        metavar="W",
        help="number of data loading workers (default: 2)",
    )
    parser.add_argument(
        "--epochs",
        type=int,
        default=2,
        metavar="E",
        help="number of total epochs to run (default: 2)",
    )
    parser.add_argument(
        "--batch_size",
        type=int,
        default=4,
        metavar="BS",
        help="batch size (default: 4)",
    )
    parser.add_argument(
        "--lr",
        type=float,
        default=0.001,
        metavar="LR",
        help="initial learning rate (default: 0.001)",
    )
    parser.add_argument(
        "--momentum",
        type=float,
        default=0.9,
        metavar="M",
        help="momentum (default: 0.9)",
    )
    parser.add_argument(
        "--dist_backend",
        type=str,
        default="gloo",
        help="distributed backend (default: gloo)",
    )

    # SageMaker specific part
    # For detail please check:
    # https://github.com/aws/sagemaker-containers
    sm_hosts: Final = os.environ.get("SM_HOSTS", "")
    sm_current_host: Final = os.environ.get("SM_CURRENT_HOST", "")
    sm_model_dir: Final = os.environ.get("SM_MODEL_DIR", "outputs")
    sm_channel_training: Final = os.environ.get("SM_CHANNEL_TRAINING", "data")

    parser.add_argument("--hosts", type=list, default=sm_hosts)  # type: ignore
    parser.add_argument("--current-host", type=str, default=sm_current_host)
    parser.add_argument("--model-dir", type=str, default=sm_model_dir)
    parser.add_argument("--data-dir", type=str, default=sm_channel_training)

    _train(parser.parse_args())
