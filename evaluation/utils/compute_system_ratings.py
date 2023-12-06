import pandas as pd

def main():

    for dialect in ["be", "zh"]:
        data = pd.read_csv(f"../ntrex-128/human-scores/en-gsw_{dialect}.ntrex-128.seg.score", sep="\t", header=None, names=["system", "score"]) 
        data.groupby("system").mean().to_csv(f"../ntrex-128/human-scores/en-gsw_{dialect}.ntrex-128.sys.score", sep="\t", header=False)

if __name__ == "__main__":
    main()
    