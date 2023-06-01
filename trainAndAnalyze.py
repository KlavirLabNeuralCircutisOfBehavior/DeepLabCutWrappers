import sys

from analyzeVideos import analyze
from trainDeepLabCut import train


def main():
    train(*sys.argv[1:5])
    analyze(*sys.argv[5:])
    print("done full run")

if __name__ == "__main__":
    main()