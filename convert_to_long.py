import readmat from scipy.io

def write_to_file(filename, contents):
    """Writes a string to a file."""
    _file = open(filename, 'w')
    _file.write(out)
    _file.close

def make_row(*L):
    "Creates a tab-separated row."
    return "\t".join(str(elt) for elt in L) + "\n"

if __name__ == "__main__":
    data = readmat("fdata_lpp.mat")
    
    # Pull out data from `data`
    labels = [label[0][0] for label in data['labels']]
    resps = data['presps']
    
    # Convert `data['presps']` into a dict, addressable by segment name.
    resp_dict = {}
    for i, segment in enumerate(labels):
        resp_dict[segment] = resps[i][0]
    
    # Convert to long format. Each observation on a row.
    out = ""
    for label in labels:
        # Omit oy because it only has 1 trial.
        if label == "oy": continue
        segment = resp_dict[label]
        trials = 0
        neurons, bins, trials = segment.shape
        print label

        for neuron in xrange(neurons):
            for bin in xrange(bins):
                for trial in xrange(trials):
                    out += make_row(label, neuron, bin, trial, segment[neuron, bin, trial])

    write_to_file("ferret_data.txt", 'w')
        
    