import os
import os.path
import sys
import glob
import argparse
import helper

import libml
from model import Model
from note import *

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", 
    dest = "input", 
    help = "The input files to predict", 
    default = os.path.join(os.path.dirname(os.path.realpath(__file__)), '../data/test_data/*')
    )

    parser.add_argument("-o", 
    dest = "output", 
    help = "The directory to write the output", 
    default = os.path.join(os.path.dirname(os.path.realpath(__file__)), '../data/test_predictions')
    )

    parser.add_argument("-m",
        dest = "model",
        help = "The model to use for prediction",
        default = os.path.join(os.path.dirname(os.path.realpath(__file__)), '../models/run_models/run.model')
    )

    parser.add_argument("--no-svm",
        dest = "no_svm",
        action = "store_true",
        help = "Disable SVM model generation",
    )

    parser.add_argument("--no-lin",
        dest = "no_lin",
        action = "store_true",
        help = "Disable LIN model generation",
    )

    parser.add_argument("--no-crf",
        dest = "no_crf",
        action = "store_true",
        help = "Disable CRF model generation",
    )

    args = parser.parse_args()

    # Locate the test files
    files = glob.glob(args.input)

    # Load a model and make a prediction for each file
    path = args.output
    helper.mkpath(args.output)

    # Load model
    model = Model.load(args.model)


    # file names
    print files


    for txt in files:

        # Read the data into a Note object
        note = Note()
        note.read_i2b2(txt)
        #note.read_plain(txt)   # TEMP - in case of plain format


        # Use the model to predict the concept labels
        # Returns a hash table with:
        #     keys as 1,2,4
        #     values as list of list of concept tokens (one-to-one with dat_list)
        try:
            labels = model.predict(note)
        except IndexError:  # FIXME - Not sure what causes this (something GENIA-related)
            continue


        con = os.path.split(txt)[-1]
        con = con[:-3] + 'con'

        for t in libml.bits(model.type):

            # FIXME - workaround. I'm not sure why it doesnt make some 
            if t not in labels: 
                continue

            if t == libml.SVM:
                helper.mkpath(os.path.join(args.output, "svm"))
                con_path = os.path.join(path, "svm", con)
            if t == libml.LIN:
                helper.mkpath(os.path.join(args.output, "lin"))
                con_path = os.path.join(path, "lin", con)


            # Output the concept predictions
            output = note.write_i2b2_con(labels[t])
            with open(con_path, 'w') as f:
                print >>f, output
            #note.write_plain(con_path, labels[t])   # in case of plain format

            #note.write_BIOs_labels(con_path, labels[t])



if __name__ == '__main__':
    main()
