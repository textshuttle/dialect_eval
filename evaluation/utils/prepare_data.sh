NTREX_DIR=../ntrex-128/raw

# Only uncomment if you want to extract from the unzipped data
#unzip $NTREX_DIR/references_be_zh.zip -d $NTREX_DIR/
#rm -r $NTREX_DIR/__MACOSX # Clean up 

for dialect in be zh;do
    python3 extract_ntrex_refs.py --dialect $dialect
    python3 extract_segment_ratings.py --dialect $dialect
    python3 compute_scores.py --dialect $dialect
done

python3 compute_system_ratings.py
