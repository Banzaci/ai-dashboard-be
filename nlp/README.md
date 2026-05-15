python train.py
python -m spacy init config config.cfg --lang en --pipeline textcat,ner --force
python -m spacy train config.cfg \                                  ✔  fastapi   08:32:21 
  --output ./model \
  --paths.train data/train.spacy \
  --paths.dev data/train.spacyp


  spacy train config.cfg \
  --output ./model \
  --paths.init_tok2vec ./model/model-best