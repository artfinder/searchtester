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
    # achieved with a position of 0, decreasing exponentially
    # (since there is no maximum), with a contribution of 0 if
    # the position is None.
    
    score = 0
    max_available_score = 0
    for expected, actual in enumerate(positions):
        try:
            actual = int(actual)
        except:
            actual = None
        max_score = math.exp(-expected)
        max_available_score += max_score
        
        if actual is not None:
            score += max_score * math.exp(-actual)
    if max_available_score == 0:
        # no positions passed through; somewhat arbitrary, but
        # let's call that 0
        return 0
    else:
        return score / max_available_score
