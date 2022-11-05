from enum import Enum
import openpyxl


class Label(Enum):
    POSITIVE = "pos"
    NEGATIVE = "neg"

class Review:
    def __init__(self, text: str, label: str):
        self.text = text
        self.label = label

    def __str__(self):
        return str(self.label) + " " + str(self.text)


def resolve_label(score_and_max: str) -> str:
    scores_str = score_and_max.replace(',', '.').split('/')

    max_score = int(scores_str[1])
    score = float(scores_str[0])

    if score <= 0 or score > max_score:
        raise Exception("Invalid scores")

    return Label.NEGATIVE.value if score < max_score / 2 else Label.POSITIVE.value


def parse_reviews(file_name: str) -> [Review]:
    reviews: [Review] = []

    file = openpyxl.load_workbook(file_name, data_only=True).active

    for row in file.iter_rows(min_row=2, min_col=2, max_col=3):
        label = resolve_label(row[1].value)
        review_description = row[0].value \
            .replace('\n', ' ') \
            .replace('<br>', ' ') \
            .replace('</br>', ' ') \
            .replace('<br/>', ' ')

        reviews.append(Review(review_description, label))

    return reviews
