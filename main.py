from torchtext.data.utils import get_tokenizer
from torchdata.datapipes.iter import IterableWrapper, FileOpener, IterDataPipe, T_co


class _ParseCustomDataset(IterDataPipe):
    def __getitem__(self, index) -> T_co:
        pass

    def __init__(self, source_datapipe) -> None:
        self.source_datapipe = source_datapipe

    def __iter__(self):
        for _, raw_json_data in self.source_datapipe:
            for element in raw_json_data:
                yield element['label'], element['text']


if __name__ == "__main__":
    dp = IterableWrapper(["ProcessedDatasets/train.json"])
    dp = FileOpener(dp, mode='b')
    dp = dp.parse_json_files()

    e = _ParseCustomDataset(dp)

    train_iter = iter(e)

    print(next(train_iter))

    get_tokenizer('spacy', 'pl_core_news_md')
