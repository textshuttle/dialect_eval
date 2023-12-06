from argparse import ArgumentParser

import pandas as pd

CSV_HEADER = [
    "rater_id",
    "model_id",
    "segment_id",
    "is_control",
    "src_lang",
    "trg_lang",
    "score",
    "doc_id",
    "is_doclevel",
    "start_time",
    "end_time",
]

BE_SYSTEMS = ["1_degsw", "1_endegsw", "2_degsw", "2_endegsw", "3_degsw", "3_endegsw", "3_engsw", "4_degsw", "4_endegsw"]
ZH_SYSTEMS = ["0_degsw", "0_endegsw", "1_degsw", "2_endegsw", "3_degsw", "3_endegsw", "3_engsw", "4_degsw", "4_endegsw"]

BE_MODEL_IDS = {
    "model-1-de": "1_degsw",
    "model-1-ende": "1_endegsw",
    "model-2-de": "2_degsw",
    "model-2-ende": "2_endegsw",
    "model-3-de": "3_degsw",
    "model-3-ende": "3_endegsw",
    "model-3-en": "3_engsw",
    "model-4-de": "4_degsw",
    "model-4-ende": "4_endegsw",
}

ZH_MODEL_IDS = {
    "model-0-de": "0_degsw",
    "model-0-ende": "0_endegsw",
    "model-1-de": "1_degsw",
    "model-2-ende": "2_endegsw",
    "model-3-de": "3_degsw",
    "model-3-ende": "3_endegsw",
    "model-3-en": "3_engsw",
    "model-4-de": "4_degsw",
    "model-4-ende": "4_endegsw",
}

def parse_args():
    parser = ArgumentParser()
    parser.add_argument("--dialect", "-d", default='zh', type=str)
    return parser.parse_args()

def main(args):
    data = pd.read_csv(
        f"../ntrex-128/raw/ratings/{args.dialect}/scores.csv",
        names=CSV_HEADER,
    )
    # Exclude the control segments; not sure what the is_doclevel == True segments are
    data = data[(data["is_control"] == "TGT") & (data["is_doclevel"] == False) & (data["model_id"] != "model-5-de")]

    sanity_checks = True
    if sanity_checks:
        check_model_id = None

    print(data)

    with open(f"../ntrex-128/human-scores/en-gsw_{args.dialect}.ntrex-128.seg.score", "w") as output_file:

        for df in data.groupby(["model_id", "doc_id"]):

            model_doc_data = df[1]

            if sanity_checks:
                
                # Check that the model and doc ids are unique (a bit redundant but better safe than sorry)    
                assert len(model_doc_data["doc_id"].unique()) == 1
                assert len(model_doc_data["model_id"].unique()) == 1
                
                # Check if the count needs to be reset to check the doc_ids
                raw_model_id = model_doc_data["model_id"].unique()[0]
                if raw_model_id != check_model_id:
                    check_model_id = raw_model_id
                    check_doc_id = 0

                # Check that the doc_ids are in the correct order when going throgugh them
                # First extract the full id and then get the doc id from it
                full_id = model_doc_data["doc_id"].unique()[0]
                assert int(full_id.split("_")[0]) - 1 == check_doc_id
                check_doc_id += 1

            # Sort by segment id to match the order of the segments in the reference file
            # Sort by start_time after to be able to keep the last segment when dropping segment_id duplicates (i.e. keep the latest version of the rating)
            model_doc_data = model_doc_data.sort_values(by=["segment_id"])#, "start_time"])
            model_doc_data["mean_score"] = model_doc_data.groupby('segment_id')['score'].transform('mean')
            model_doc_data.drop_duplicates(subset=["segment_id"], keep="last", inplace=True)

            segments_per_doc = model_doc_data["segment_id"].tolist()[-1]

            if len(model_doc_data["mean_score"].tolist()) != int(segments_per_doc) + 1:
                print(model_doc_data)

            if args.dialect == "zh":
                model_ids = ZH_MODEL_IDS
            elif args.dialect == "be":
                model_ids = BE_MODEL_IDS

            model_id = model_ids[model_doc_data["model_id"].unique()[0]]

            for score in model_doc_data["mean_score"].tolist():         
                output_file.write(f"{model_id}\t{score}\n")

if __name__ == "__main__":
    args = parse_args()
    main(args)
