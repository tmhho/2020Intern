#!/bin/bash
filenames=`ls`
for file in $filenames; 
do
fileout=(${file//:/_}) ;
fileout="${fileout}.png"
mv $file $fileout;
done;
