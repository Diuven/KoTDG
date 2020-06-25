source env/bin/activate

echo "Generating preconfigured ksx1001 (Fixed) dataset!"
echo "224x224, black text color, clean white background, 2350 classes, random easy fonts"

COUNT20=2000
RTRAIN=17
RVALID=2
RTESTS=1
DIR="out/ksxfix/"
FONTDIR="resources/fonts/easy"
THREADS=32

echo "Generating train dataset"
python3 run.py --height 224 --width 224 --background 1 -t $THREADS --output_dir $DIR/train --font_dir $FONTDIR --count $(expr $COUNT20 "*" $RTRAIN)

echo "Generating validation dataset"
python3 run.py --height 224 --width 224 --background 1 -t $THREADS --output_dir $DIR/valid --font_dir $FONTDIR --count $(expr $COUNT20 "*" $RVALID)

echo "Generating test dataset"
python3 run.py --height 224 --width 224 --background 1 -t $THREADS --output_dir $DIR/tests --font_dir $FONTDIR --count $(expr $COUNT20 "*" $RTESTS)
