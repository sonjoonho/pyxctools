import argparse
from pyxctools.xenocanto import XenoCanto

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-q", "--query", help="Basic search terms.", required=True)

    parser.add_argument("-p", "--page", type=int, default=None, help="Page number.", required=False)
    parser.add_argument("-d", "--dir", type=str, default="sounds", help="Directory to download to.", required=False)

    args = parser.parse_args()

    xc = XenoCanto()

    xc.download_files(search_terms=args.query, page=args.page, dir=args.dir)
