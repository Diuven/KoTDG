source env/bin/activate

echo "Generating preconfigured ksx1001 (Augmented) dataset!"
echo "224x224, random color, random background, 2350 classes, random hard fonts"

COUNT20=20000
RTRAIN=17
RVALID=2
RTESTS=1
DIR="out/ksxaug/"
FONTDIR="resources/fonts/easy"
THREADS=32

echo "Generating train dataset"
python3 run.py --height 224 --width 224 --rand_color --rand_back -t $THREADS --output_dir $DIR/train --font_dir $FONTDIR --count $(expr $COUNT20 "*" $RTRAIN)

echo "Generating validation dataset"
python3 run.py --height 224 --width 224 --rand_color --rand_back -t $THREADS --output_dir $DIR/valid --font_dir $FONTDIR --count $(expr $COUNT20 "*" $RVALID)

echo "Generating test dataset"
python3 run.py --height 224 --width 224 --rand_color --rand_back -t $THREADS --output_dir $DIR/tests --font_dir $FONTDIR --count $(expr $COUNT20 "*" $RTESTS)
