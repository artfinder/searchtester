import math

def calculate_score(positions):
    """
    Takes a list of zero-indexed positions and returns
    a score between 0.0 and 1.0. The positions are actual
    result positions, but the indexes of the positions array
    are where the results *should* have been. So:
    
    [ 0, 1, 2, 3, 4 ] is perfect
    [ 1, 0, 2, 3, 4 ] means the first two results are flipped
    
    A position of None means "not found" (on the first page of
    results, currently).
    """

    # The positions are of decreasing importance, so we want to
    # apportion contributions to the score using an exponential
    # decay function. Then within that, maximum score is always
    # achieved with a position of the highest not yet found,
    # decreasing exponentially (since there is no maximum),
    # with a contribution of 0 if the position is None.
    
    # print "calculate_score", positions
    
    score = 0
    max_available_score = 0
    found = {} # position -> True
    for expected, actual in enumerate(positions):
        try:
            actual = int(actual)
        except:
            actual = None
        max_score = math.exp(-expected)
        max_available_score += max_score
        
        if actual is not None:
            # we need to convert actual in a 0-indexed
            # offset into the list of unfound positions
            use = 0
            for idx in range(0, actual):
                # print "--", idx, found.get(idx, False)
                if not found.get(idx, False):
                    use += 1
            # print expected, actual, use
            score += max_score * math.exp(-use)
            found[actual] = True
    if max_available_score == 0:
        # no positions passed through; somewhat arbitrary, but
        # let's call that 0
        return 0
    else:
        return score / max_available_score
