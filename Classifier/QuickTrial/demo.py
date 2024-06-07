import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader
import torchvision.transforms as transforms
from torchvision.models import resnet18,resnet50
from torchvision.datasets import ImageFolder # 导入ImageFolder类，用来根据文件夹名划分类别
import pytorch_lightning as pl # 导入pytorch_lightning

# 定义一个继承自pl.LightningDataModule的类，用来封装数据集的下载、预处理、划分和加载
class ImageFolderDataModule(pl.LightningDataModule):
    def __init__(self, batch_size, data_dir: str = '/Users/kennymccormick/Downloads/0603四月份钴60验货照片'):
        super().__init__()
        self.data_dir = data_dir # 数据集的根目录，假设是./data
        self.batch_size = batch_size # 批次大小
        self.transform = transforms.Compose([ # 定义数据预处理，包括缩放、裁剪、转换为张量和归一化
            transforms.Resize((120, 1024)),
            transforms.ToTensor(),
            transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))
        ])

    def prepare_data(self):
        # 下载或处理数据，只在一个进程中执行一次，不需要返回值
        pass

    def setup(self, stage=None):
        # 划分数据集为训练集和验证集，可以在每个进程中执行多次，需要设置属性
        dataset = ImageFolder(self.data_dir, transform=self.transform) # 创建ImageFolder数据集
        train_size = int(0.8 * len(dataset)) # 训练集大小，假设是80%
        val_size = len(dataset) - train_size # 验证集大小，假设是20%
        self.train_dataset, self.val_dataset = torch.utils.data.random_split(dataset, [train_size, val_size], generator=torch.Generator().manual_seed(42)) # 划分数据集，设置随机种子为42

    def train_dataloader(self):
        # 返回训练集加载器
        return DataLoader(self.train_dataset, batch_size=self.batch_size, shuffle=True, num_workers=2)

    def val_dataloader(self):
        # 返回验证集加载器
        return DataLoader(self.val_dataset, batch_size=self.batch_size, shuffle=False, num_workers=2)

# 定义一个继承自pl.LightningModule的类，用来定义和训练模型
class ResNet18Classifier(pl.LightningModule):
    def __init__(self):
        super().__init__()
        self.model = resnet50() # 加载预训练的resnet18模型,pretrained=True
        self.model.fc = nn.Linear(self.model.fc.in_features, 4) # 修改最后一层为全连接层，输出类别数为10
        self.criterion = nn.CrossEntropyLoss() # 定义交叉熵损失函数

    def forward(self, x):
        return self.model(x) # 前向传播，得到输出

    def training_step(self, batch, batch_idx):
        inputs, labels = batch # 获取输入和标签
        outputs = self(inputs) # 前向传播，得到输出
        loss = self.criterion(outputs, labels) # 计算损失
        self.log("train_loss", loss, on_epoch=True, prog_bar=True) # 记录训练损失
        return loss

    def validation_step(self, batch, batch_idx):
        inputs, labels = batch # 获取输入和标签
        outputs = self(inputs) # 前向传播，得到输出
        loss = self.criterion(outputs, labels) # 计算损失
        acc = (outputs.argmax(dim=1) == labels).float().mean() # 计算准确率
        self.log("val_loss", loss, on_epoch=True, prog_bar=True) # 记录验证损失
        self.log("val_acc", acc, on_epoch=True, prog_bar=True) # 记录验证准确率

    def configure_optimizers(self):
        # 定义优化器，使用随机梯度下降
        return optim.Adam(self.parameters(), lr=1e-3)

if __name__ == "__main__":
    import torch.multiprocessing as mp
    mp.freeze_support()
    # 创建数据模块和模型实例
    data_module = ImageFolderDataModule(batch_size=32)
    model = ResNet18Classifier()

    # 创建训练器，指定使用mps设备
    trainer = pl.Trainer(accelerator="mps", max_epochs=10)

    # 开始训练和验证
    trainer.fit(model, data_module)
