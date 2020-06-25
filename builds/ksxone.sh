source env/bin/activate

echo "Generating preconfigured ksx1001 (Single Font) dataset!"
echo "224x224, black text color, clean white background, 2350 classes, single font (NanumGothicBold.ttf)"

COUNT20=500
RTRAIN=17
RVALID=2
RTESTS=1
DIR="out/ksxone/"
FONT="NanumGothicBold.ttf"
THREADS=32

echo "Generating train dataset"
python3 run.py --height 224 --width 224 --background 1 -t $THREADS --output_dir $DIR/train --font $FONT --count $(expr $COUNT20 "*" $RTRAIN)

echo "Generating validation dataset"
python3 run.py --height 224 --width 224 --background 1 -t $THREADS --output_dir $DIR/valid --font $FONT --count $(expr $COUNT20 "*" $RVALID)

echo "Generating test dataset"
python3 run.py --height 224 --width 224 --background 1 -t $THREADS --output_dir $DIR/tests --font $FONT --count $(expr $COUNT20 "*" $RTESTS)
