import time
from typing import Union, Tuple

import torch
from torch.utils.data import DataLoader, random_split, functional_datapipe
from torchtext.data import to_map_style_dataset
from torchtext.data.datasets_utils import _wrap_split_argument
from torchtext.data.utils import get_tokenizer
from torchdata.datapipes.iter import IterableWrapper, FileOpener, IterDataPipe
from torchtext.datasets import AG_NEWS, IMDB, SQuAD2
from torchtext.vocab import build_vocab_from_iterator

from model import TextClassificationModel

NUM_LINES = {
    "train": 40000,
    "test": 28012,
}


@functional_datapipe("read_dataset")
class ParseCustomDataset(IterDataPipe):

    def __init__(self, source_datapipe) -> None:
        self.source_datapipe = source_datapipe

    def __iter__(self):
        for _, raw_json_data in self.source_datapipe:
            for element in raw_json_data:
                yield element['label'], element['text']


@_wrap_split_argument(("train", "test"))
def create_dataset(root: str, split: Union[Tuple[str], str]):
    dp = IterableWrapper(["ProcessedDatasets/reviews.json"])
    dp = FileOpener(dp, mode='b')
    dp = dp.parse_json_files()
    return dp.read_dataset().shuffle().set_shuffle(False).sharding_filter()


def train(dataloader):
    model.train()
    total_acc, total_count = 0, 0
    log_interval = 500
    start_time = time.time()

    for idx, (label, text, offsets) in enumerate(dataloader):
        optimizer.zero_grad()
        predicted_label = model(text, offsets)
        loss = criterion(predicted_label, label)
        loss.backward()
        torch.nn.utils.clip_grad_norm_(model.parameters(), 0.1)
        optimizer.step()
        total_acc += (predicted_label.argmax(1) == label).sum().item()
        total_count += label.size(0)
        if idx % log_interval == 0 and idx > 0:
            elapsed = time.time() - start_time
            print('| epoch {:3d} | {:5d}/{:5d} batches '
                  '| accuracy {:8.3f}'.format(epoch, idx, len(dataloader),
                                              total_acc / total_count))
            total_acc, total_count = 0, 0
            start_time = time.time()


def evaluate(dataloader):
    model.eval()
    total_acc, total_count = 0, 0

    with torch.no_grad():
        for idx, (label, text, offsets) in enumerate(dataloader):
            predicted_label = model(text, offsets)
            loss = criterion(predicted_label, label)
            total_acc += (predicted_label.argmax(1) == label).sum().item()
            total_count += label.size(0)
    return total_acc / total_count


def collate_batch(batch):
    label_list, text_list, offsets = [], [], [0]
    for (_label, _text) in batch:
        label_list.append(_label)
        processed_text = torch.tensor(text_pipeline(_text), dtype=torch.int64)
        text_list.append(processed_text)
        offsets.append(processed_text.size(0))

    label_list = torch.tensor(label_list, dtype=torch.int64)
    offsets = torch.tensor(offsets[:-1]).cumsum(dim=0)
    text_list = torch.cat(text_list)
    return label_list.to(device), text_list.to(device), offsets.to(device)


def yield_tokens(data_iter):
    for _, text in data_iter:
        yield tokenizer(text)


def predict(text, text_pipeline):
    with torch.no_grad():
        text = torch.tensor(text_pipeline(text))
        output = model(text, torch.tensor([0]))
        return output.argmax(1).item() + 1


if __name__ == "__main__":
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    dataset = create_dataset(split='train')

    tokenizer = get_tokenizer('spacy', 'pl_core_news_md')
    # tokenizer1 = get_tokenizer('basic_english')

    ########################################

    # print(yield_tokens(train_iter))
    # train_iter1 = AG_NEWS(split='train')

    vocab = build_vocab_from_iterator(yield_tokens(dataset), specials=["<unk>"])
    vocab.set_default_index(vocab["<unk>"])

    text_pipeline = lambda x: vocab(tokenizer(x))
    # label_pipeline = lambda x: int(x) - 1

    ########################################

    print(text_pipeline("super telewizor"))

    ########################################
    num_class = len(set([label for (label, text) in dataset]))

    vocab_size = len(vocab)
    emsize = 64
    model = TextClassificationModel(vocab_size, emsize, num_class).to(device)

    print(dataset)

    ########################################
    # Hyperparameters
    EPOCHS = 10  # epoch
    LR = 5  # learning rate
    BATCH_SIZE = 64  # batch size for training

    criterion = torch.nn.CrossEntropyLoss()
    optimizer = torch.optim.SGD(model.parameters(), lr=LR)
    scheduler = torch.optim.lr_scheduler.StepLR(optimizer, 1.0, gamma=0.1)
    total_accu = None
    train_iter, test_iter = create_dataset()
    train_dataset = to_map_style_dataset(train_iter)
    test_dataset = to_map_style_dataset(test_iter)
    num_train = int(len(train_dataset) * 0.95)
    split_train_, split_valid_ = \
        random_split(train_dataset, [num_train, len(train_dataset) - num_train])

    train_dataloader = DataLoader(split_train_, batch_size=BATCH_SIZE,
                                  shuffle=True, collate_fn=collate_batch)
    valid_dataloader = DataLoader(split_valid_, batch_size=BATCH_SIZE,
                                  shuffle=True, collate_fn=collate_batch)
    test_dataloader = DataLoader(test_dataset, batch_size=BATCH_SIZE,
                                 shuffle=True, collate_fn=collate_batch)

    for epoch in range(1, EPOCHS + 1):
        epoch_start_time = time.time()
        train(train_dataloader)
        accu_val = evaluate(valid_dataloader)
        if total_accu is not None and total_accu > accu_val:
            scheduler.step()
        else:
            total_accu = accu_val
        print('-' * 59)
        print('| end of epoch {:3d} | time: {:5.2f}s | '
              'valid accuracy {:8.3f} '.format(epoch,
                                               time.time() - epoch_start_time,
                                               accu_val))
        print('-' * 59)

    # print('Checking the results of test dataset.')
    # accu_test = evaluate(test_dataloader)
    # print('test accuracy {:8.3f}'.format(accu_test))
    #
    # ag_news_label = {1: "Positive",
    #                  2: "Negative"}
    #
    # ex_text_str = "Super mega TV!"
    #
    # model = model.to("cpu")
    #
    # print("This is a %s review" % ag_news_label[predict(ex_text_str, text_pipeline)])
