import argparse
from data.cdc_api.cdc_county import get_sample_data as g


def main():
    limit = 100
    parser = argparse.ArgumentParser()
    parser.add_argument('--limit', action="store", type=int, help='the limit of CDC vaccine data to retrieve')
    args = parser.parse_args()

    if args.limit: #If user enters value for limit, updates limit variable
        limit = args.limit

    vax_data = g(limit)

    print(vax_data)
    print("------------------------")


if __name__ == '__main__':
    main() 