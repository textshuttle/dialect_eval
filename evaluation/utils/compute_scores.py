from argparse import ArgumentParser

from scores import BLEUScore, CHRFScore, COMETScore
from utils import load_segments


SCORE_NAMES = {
    "bleu": BLEUScore(),
    "chrf": CHRFScore(),
    "comet-22": COMETScore("Unbabel/wmt22-comet-da"),
    "comet-qe-20": COMETScore("Unbabel/wmt20-comet-qe-da"),
    "comet-20": COMETScore("Unbabel/wmt20-comet-da"),
    "comet-qe-kiwi": COMETScore("Unbabel/wmt22-cometkiwi-da"),
}

BE_SYSTEMS = ["1_degsw", "1_endegsw", "2_degsw", "2_endegsw", "3_degsw", "3_endegsw", "3_engsw", "4_degsw", "4_endegsw", "5_degsw"]
ZH_SYSTEMS = ["0_degsw", "0_endegsw", "1_degsw", "2_endegsw", "3_degsw", "3_endegsw", "3_engsw", "4_degsw", "4_endegsw", "5_degsw"]
BE_CHALLENGE_SETS = ["sentA", "sentB", "sentA_sem_changed"]
ZH_CHALLENGE_SETS = ["sentA", "sentB", "sentA_sem_changed"]


def parse_args():
    parser = ArgumentParser()
    parser.add_argument('--dialect', required=True)
    parser.add_argument('--scores', default="all")

    return parser.parse_args()

def main(args):

    assert args.scores == "all" or args.scores in SCORE_NAMES

    if args.scores == "all":
        scores = SCORE_NAMES.keys()
    else: scores = [args.scores]
    
    # Load references
    references = load_segments(f"../ntrex-128/references/en-gsw_{args.dialect}.refA.txt")

    for score in scores:

        print(f"-------\n{score}\n-------\n")

        with open(f'../ntrex-128/metric-scores/en-gsw_{args.dialect}/{score.upper()}-refA.sys.score', 'w') as sys_score_file, \
             open(f'../ntrex-128/metric-scores/en-gsw_{args.dialect}/{score.upper()}-refA.seg.score', 'w') as seg_score_file:

            scorer = SCORE_NAMES[score]

            srcs = []

            if args.dialect == "be":
                systems = BE_SYSTEMS
            elif args.dialect == "zh":
                systems = ZH_SYSTEMS
            elif args.dialect == "challenge_set_be":
                systems = BE_CHALLENGE_SETS
            elif args.dialect == "challenge_set_zh":
                systems = ZH_CHALLENGE_SETS


            for system in systems:
                
                translations = load_segments(f"../ntrex-128/system-outputs/en-gsw_{args.dialect}/{system}.txt")
                sys_score = scorer.compute_testset_score(srcs, 
                                                translations, 
                                                references)
                print(system)
                print(sys_score)
                sys_score_file.write(f"{system}\t{sys_score}\n")

                seg_scores = scorer.compute_segments_score(srcs,translations,references)
                for seg_score in seg_scores:
                    seg_score_file.write(f"{system}\t{seg_score}\n")


if __name__ == '__main__':
    args = parse_args()
    main(args)
