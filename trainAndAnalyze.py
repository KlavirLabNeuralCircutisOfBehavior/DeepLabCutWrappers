import sys

from analyzeVideos import analyze
from trainDeepLabCut import train


def main():
    train(sys.argv[1],sys.argv[2],sys.argv[3],sys.argv[4],sys.argv[-3],sys.argv[-1])
    analyze(*sys.argv[5:])
    print("done full run")

if __name__ == "__main__":
    main()