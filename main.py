import torch
from torchtext import datasets
from torchtext.data.utils import get_tokenizer

from torchdata.datapipes.iter import IterableWrapper, FileOpener


if __name__ == "__main__":
    dp = IterableWrapper(["ProcessedDatasets/train.json"])
    dp = FileOpener(dp, mode='b')
    dp = dp.parse_json_files()

    print(type(dp))

    # for sample in dp:
    #     print(sample)

    train_iter = iter(dp)
    #
    # print(next(train_iter))

    get_tokenizer('spacy', 'pl_core_news_md')

