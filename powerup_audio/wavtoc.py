infile = "short.wav"
outfile = 'byteout.txt'
arrayName = "soundArray"

import os
import wave
import scipy.io.wavfile

for i in range(10):
    infile = str(i+1)+".wav"
    outfile = str(i+1)+'c.txt'
    arrayName = str(i+1)+"sound_arr"
    BOARD_SAMPLERATE=8000 #board is 8khz sampling

    with wave.open(infile) as fd:
        params = fd.getparams()
        frames = fd.readframes(100000000000000) # there better not be more than this many frames

    print(params)

    rate, data_np_ary = scipy.io.wavfile.read(infile)
    # print(data_np_ary.tolist())

    file_object = open(outfile, 'w')

    elementsTotal = 0
    count = 0
    for elem in data_np_ary:
        count+=1;
        if count%(params.framerate//BOARD_SAMPLERATE) == 0:
            elementsTotal+=1
    file_object.write('const int '+arrayName+'['+str(elementsTotal)+']['+str(params.nchannels)+'] = {')


    count = 0
    elements = 0
    for elem in data_np_ary:
        count+=1;
        if count%(params.framerate//BOARD_SAMPLERATE) == 0:
            elements+=1
            if (params.nchannels == 2):
                if(elem[0] != 0 or elem[1] != 0):
                    file_object.write('{' + elem[0].astype(str) + ', ' + elem[1].astype(str)+'},')
                    if count%((params.framerate//BOARD_SAMPLERATE)*20) == 0: # 20 LR samples per line
                        file_object.write('\n')
            else:
                file_object.write( elem.astype(str) + ',')
                if count%((params.framerate//BOARD_SAMPLERATE)*20) == 0: # 20 LR samples per line
                    file_object.write('\n')


    if (params.nchannels == 2):
        file_object.write('{0,0}};')
    else:
        file_object.write('0};')

    file_object.close()
    print("created array of " +str(elementsTotal) +" elements")
