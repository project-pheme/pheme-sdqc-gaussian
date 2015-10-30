JSON_MSG=kafka_example1.txt #~/workspace/rumour_data/tweet-level-judgment/pheme-final-dataset/threads/en/ferguson/500307001629745152/reactions/500315576460668929.json
TEXTPY_PATH=text.py
BROWNCLUSTERS_PATH=data/resources/50mpaths2
MODEL_PATH=results/store_models_test/BROWNGPjoinedfeaturesPooledLIN0.pick
TRAINING_DATA_PATH=data/twoPHEME_datasets_as_events_041015.csv
OUTPATH=kafka_out.txt


mytime="$(time cat $JSON_MSG | python $TEXTPY_PATH -t txt -r text -p 19,0,15,5,3,6,4,20,8 -w BROWN_STR -b $BROWNCLUSTERS_PATH -j lines | python add_misinformation_to_json.py $MODEL_PATH $TRAINING_DATA_PATH $OUTPATH)"
echo "$mytime"
