import argparse
from cdc import DataCollector

def main():
    collector = DataCollector()
    limit = 200 
    parser = argparse.ArgumentParser()
    parser.add_argument('--limit', action="store", type=int, help='the limit of the number of vaccine data to receive')
    parser.add_argument('--des', action='store_true', help='Sort vaccine info by state in Z to A order (default: ascending order)')
  
    args = parser.parse_args()
    
    if args.limit: #If user enters value for limit, updates limit variable
        limit = args.limit
    
    vax_data = collector.get_data(limit)

    if args.des:
        vax_data.sort(reverse=True, key=lambda obj: obj.location)
    else:
        vax_data.sort(key=lambda obj: obj.location)

    for result in vax_data:
        print(result)
        print("------------------------")


if __name__ == '__main__':
    main() 