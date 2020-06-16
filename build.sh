#! /usr/bin/zsh

echo "Generating preconfigured ksx1001 dataset!"
echo "224x224, random color, random background, 2350 classes, random fonts"

COUNT20=20000
RTRAIN=17
RVALID=2
RTESTS=1
DIR="out/test/"
FONTDIR="resources/fonts"
THREADS=32

echo "Generating train dataset"
./run.py --height 224 --width 224 --rand_color --rand_back -t $THREADS --output_dir $DIR/train --font_dir $FONTDIR --count $(expr $COUNT20 "*" $RTRAIN)

echo "Generating validation dataset"
./run.py --height 224 --width 224 --rand_color --rand_back -t $THREADS --output_dir $DIR/valid --font_dir $FONTDIR --count $(expr $COUNT20 "*" $RVALID)

echo "Generating test dataset"
./run.py --height 224 --width 224 --rand_color --rand_back -t $THREADS --output_dir $DIR/tests --font_dir $FONTDIR --count $(expr $COUNT20 "*" $RTESTS)
