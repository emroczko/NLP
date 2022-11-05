import argparse
import datasets_manager as dm

parser = argparse.ArgumentParser()
parser.add_argument("-d", "--dataset", help="Show Output")
args = parser.parse_args()

if args.dataset:
    print("Dataset file: " + args.dataset)
    reviews = dm.parse_reviews(args.dataset)

    for review in reviews:
        print(vars(review))