from sacrebleu.metrics import BLEU, CHRF
from comet import download_model, load_from_checkpoint

class Score:

    def __init__(self):
        raise NotImplementedError

    def compute_testset_score(sources, translations, references):
        raise NotImplementedError

    def compute_segments_score(sources, translations, references):
        raise NotImplementedError


class BLEUScore(Score):

    def __init__(self):
        self.system_bleu = BLEU()
        self.segment_bleu = BLEU(effective_order=True)

    def compute_testset_score(self, sources, translations, references):
        return round(self.system_bleu.corpus_score(translations, [references]).score, 2)

    def compute_segments_score(self, sources, translations, references):
        return [round(self.segment_bleu.sentence_score(translation, [reference]).score, 2) for translation, reference in zip(translations, references)]

class CHRFScore(Score):
    
    def __init__(self):
        self.chrf = CHRF(word_order=2)
    
    def compute_testset_score(self, sources, translations, references):
        return round(self.chrf.corpus_score(translations, [references]).score, 2)

    def compute_segments_score(self, sources, translations, references):
        return [round(self.chrf.corpus_score(translation, [reference]).score, 2) for translation, reference in zip(translations, references)]


class COMETScore(Score):
    
    def __init__(self, path):
        if path.startswith("Unbabel"):
            self.comet_path = download_model(path)
            self.comet_model = load_from_checkpoint(self.comet_path)
        else:
            self.comet_model = load_from_checkpoint(path)
    
    def predict_comet(self, sources, translations, references):
        src_mt_ref = []
        tmp_dict = {}
        for s, t, r in zip(sources, translations, references):
            tmp_dict = {"src":s, "mt":t, "ref":r}
            src_mt_ref.append(tmp_dict)
        pred_obj =  self.comet_model.predict(src_mt_ref, batch_size=8, gpus=1) 
        segment_scores = pred_obj[0] # first element of prediction object 
        system_score = pred_obj[-1] # last element of prediction object
        return segment_scores, system_score

    def compute_testset_score(self, sources, translations, references):
        return self.predict_comet(sources, translations, references)[-1]
    
    def compute_segments_score(self, sources, translations, references):
        return self.predict_comet(sources, translations, references)[0]
