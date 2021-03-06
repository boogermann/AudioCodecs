#!/usr/bin/python3

import sys
import signal
import wave
import getopt
import alsaaudio

from ctypes import *

# opn2 = CDLL("./libOPNMIDI.so")
opn2 = CDLL("/usr/local/lib/libOPNMIDI.so")

#class OPN2MIDI_AudioFormat(Structure):
#     _fields_ = [("type", c_int),
#                 ("containerSize", c_uint),
#                 ("outasampleOffset", c_uint)]

playing = True

# Allows to quit by Ctrl+C
def catch_signal(signum, frame):
    global playing
    playing = False
    print("Caught Ctrl+C!")

def play(device, MIDIPlay, sampleRate):
    global playing

    # Opening ALSA output device
    device = alsaaudio.PCM(device=device)

    # Set attributes
    device.setchannels(2)
    device.setrate(sampleRate)
    device.setperiodsize(512)

    # format = OPN2MIDI_AudioFormat(0, 2, 4);
    device.setformat(alsaaudio.PCM_FORMAT_S16_LE)

    # Preparing the audio output buffer
    data = create_string_buffer(4096 * 2);
    dataLen = 4096

    print("Streaming...")

    # Streaming the audio data into ALSA output
    while playing:
        got = opn2.opn2_play(MIDIPlay, dataLen, cast(data, POINTER(c_short)));
        if got <= 0:
            break;
        device.write(bytearray(data.raw))

    # Closing the audio output device
    device.close()

    print("Quiting...")


def usage():
    print('usage: playmidi.py <file>', file=sys.stderr)
    sys.exit(2)

if __name__ == '__main__':
    device = 'default'
    sampleRate = 44100

    opts, args = getopt.getopt(sys.argv[1:], 'd:')
    for o, a in opts:
        if o == '-d':
            device = a

    if not args:
        usage()

    midiFile = args[0]

    # Initialize the library
    MIDIPlay = opn2.opn2_init(sampleRate)

    opn2.opn2_openBankFile(MIDIPlay, "../../fm_banks/xg.wopn".encode())

    # ============= Optional setup ====================
    # Turn on looping (optionally)
    # opn2.opn2_setLoopEnabled(MIDIPlay, 1)

    # Changing the bank number (optionally)
    # if opn2.opn2_setBank(MIDIPlay, 68) < 0:
    #    print(c_char_p(opn2.opn2_errorInfo(MIDIPlay)).value)
    #    sys.exit(1)
    # ============= Optional setup =End================

    # Open music file...
    if opn2.opn2_openFile(MIDIPlay, midiFile.encode()) < 0:
        print(c_char_p(opn2.opn2_errorInfo(MIDIPlay)).value)
        sys.exit(1)

    print("Playing MIDI file %s..." % (midiFile))

    # Allows to quit by Ctrl+C
    signal.signal(signal.SIGINT, catch_signal)

    # Start the audio streaming
    play(device, MIDIPlay, sampleRate)

    # Closing the library
    opn2.opn2_close(MIDIPlay)

