# python examples/interactive.py -m transformer/polyencoder \
#     -mf zoo:pretrained_transformers/poly_model_huge_wikito/model \
#     --encode-candidate-vecs true \
#     --eval-candidates fixed  \
#     --fixed-candidates-path data/models/pretrained_transformers/JHUcorona.txt
#     --single-turn True

echo "CROSSENCODER" > eval.txt
python examples/eval_model.py -m transformer/crossencoder \
    -mf zoo:pretrained_transformers/cross_model_huge_wikito/model -t convai2 >> eval.txt
# echo "BERT-RANKER-BIENCODER" > eval.txt
# python examples/eval_model.py -m bert_ranker/bi_encoder_ranker -mf zoo:wizard_of_wikipedia/full_dialogue_retrieval_model/model -t convai2 >> eval.txt
echo "BERT-RANKER-BIENCODER" >> eval.txt
python examples/eval_model.py -m bert_ranker/bi_encoder_ranker -t convai2 >> eval.txt
echo "POLYENCODER" >> eval.txt
python examples/eval_model.py -m transformer/polyencoder \
    -mf zoo:pretrained_transformers/poly_model_huge_wikito/model -t convai2 >> eval.txt
echo "BIENCODER" >> eval.txt
python examples/eval_model.py -m transformer/biencoder \
    -mf zoo:pretrained_transformers/bi_model_huge_wikito/model -t convai2 >> eval.txt