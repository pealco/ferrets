from scipy.io import loadmat
from numpy import *
import numpy
import time

def write_to_file(filename, contents):
    """Writes a string to a file."""
    _file = open(filename, 'w')
    _file.write(out)
    _file.close

def make_row(*L):
    "Creates a tab-separated row."
    return "\t".join(str(elt) for elt in L) + "\n"

def convert_to_long(labels, resp_dict):
    out = ""
    for label in labels:
        # Omit oy because it only has 1 trial.
        if label == "oy":     continue
        # Omit "closures"
        if label[1:] == "cl": continue
        # Omit othe crap
        if label == "pau":    continue
        if label == "epi":    continue
        
        segment = resp_dict[label]
        neurons, bins, trials = segment.shape
        print label

        for neuron in xrange(neurons):
            for bin in xrange(bins):
                for trial in xrange(trials):
                    out += make_row(label, neuron, bin, trial, segment[neuron, bin, trial])
    return out

# Mutual information functions
def entropy(counts):
    '''Compute entropy.'''
    ps = counts/float(sum(counts))  # coerce to float and normalize
    ps = ps[nonzero(ps)]            # toss out zeros
    H = -sum(ps * numpy.log2(ps))   # compute entropy

    return H

def mi(x, y, bins):
    '''Compute mutual information'''
    counts_xy = histogram2d(x, y, bins=bins)[0]
    counts_x  = histogram(  x,    bins=bins)[0]
    counts_y  = histogram(  y,    bins=bins)[0]

    H_xy = entropy(counts_xy)
    H_x  = entropy(counts_x)
    H_y  = entropy(counts_y)

    return H_x + H_y - H_xy

def mirror(data):
    n_chan = shape(data)[0]
    for c1 in range(n_chan):
        for c2 in range(n_chan):
            if c1 > c2:
                data[c1,c2] = data[c2,c1]
                data[c1,c2] = data[c2,c1]
    return data

def cross_mi(epochs, interest_cond, n_chan, bins):
    the_mi = zeros((n_chan, n_chan))
    for ch1 in range(n_chan):
        print ch1
        for ch2 in range(n_chan):
            if ch2 >= ch1:
                mi_a = epochs[:, ch1, :].flatten() ** 2
                mi_b = epochs[:, ch2, :].flatten() ** 2

                the_mi[ch1, ch2] = mi(mi_a, mi_b, bins=bins)
    return mirror(the_mi)

def auto_mi(epochs, total_offset, interest_region, n_chan, bins):
    the_mi = zeros((n_chan, total_offset))
    for ch in range(n_chan):
        print ch
        for tau in range(total_offset):
            mi_a = epochs[7, interest_region,     ch, :].flatten()
            mi_b = epochs[7, interest_region+tau, ch, :].flatten()
            ami_ldif[ch, tau] = mi(ldif_a, ldif_b, bins=bins)
    return ami_ldif

if __name__ == "__main__":
    data = loadmat("fdata_lpp.mat")
    
    # Pull out data from `data`
    labels = [label[0][0] for label in data['labels']]
    stims = data['pstims']
    resps = data['presps']
    
    # Convert `data` into a dict, addressable by segment name.
    resp_dict = {}
    stim_dict = {}
    for i, segment in enumerate(labels):
        # Omit oy because it only has 1 trial.
        if segment == "oy":     continue
        # Omit "closures"
        if segment[1:] == "cl": continue
        # Omit othe crap
        if segment == "pau":    continue
        if segment == "epi":    continue
        
        stim_dict[segment] = stims[i][0]
        resp_dict[segment] = resps[i][0]
    
    mi_dict = {}
    for label in labels:
        mi_dict[label] = mi(stim_dict[segment], resp_dict[segment])
    
    print mi_dict
        
    
    
    
    
    
    # Convert to long format. Each observation on a row.
    #out = convert_to_long(labels, resp_dict)
    #write_to_file("ferret_data.txt", out)
        
    