import numpy as np

import librosa

from evdetect.hidden_markov_models import PitchSequenceModel
from utils import import_annotations, export_subsequences


def birds():
    filename_filtered = '../examples/data/birds_filtered.wav'
    filename_annotations = '../examples/data/birds.lab'
    filename = '../examples/data/birds.wav'

    y, fs = librosa.load(filename)
    spectrum = np.abs(librosa.stft(y))
    x = spectrum.transpose()

    y_filtered, fs_filtered = librosa.load(filename_filtered)
    spectrum_filtered = np.abs(librosa.stft(y_filtered))
    x_filtered = spectrum_filtered.transpose()

    assert(fs == fs_filtered)

    hop_length = 2048 // 4

    annotations = import_annotations(filename_annotations)

    cui_specs1 = []
    cui_specs2 = []

    for i in range(len(annotations) - 1):
        spec = x_filtered[int(annotations[i] * fs / hop_length):int(annotations[i + 1] * fs / hop_length)]
        if i % 2 == 0:
            cui_specs1.append(spec.mean(axis=0))
        else:
            cui_specs2.append(spec.mean(axis=0))

    cui_spec1 = np.array(cui_specs1).mean(axis=0)
    cui_spec1 = cui_spec1 / np.sum(cui_spec1)
    cui_spec2 = np.array(cui_specs2).mean(axis=0)
    cui_spec2 = cui_spec2 / np.sum(cui_spec2)

    a = np.array([[0.5, 0.5], [0.5, 0.5]])
    pi = np.array([1, 0])
    scaling_factor = 1.4

    model = PitchSequenceModel(a, pi, np.array([cui_spec1, cui_spec2]), scaling_factor)

    epsilon = 0.05
    delta = 1

    reported_subsequences = model.detect_event(x, epsilon, delta)

    export_subsequences(reported_subsequences, fs, hop_length, '../examples/results/birds.lab')


birds()
