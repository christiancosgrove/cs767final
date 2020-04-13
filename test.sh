python examples/interactive.py -m transformer/biencoder \
    -mf zoo:pretrained_transformers/bi_model_huge_wikito/model \
    --encode-candidate-vecs true \
    --eval-candidates fixed  \
    --fixed-candidates-path data/models/pretrained_transformers/qorona.txt
    --single-turn True