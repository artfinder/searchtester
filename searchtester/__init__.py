__ALL__ = [ 'core', 'scoring' ]

def runtest():
    from searchtester.core import SearchSystemTest
    from optparse import OptionParser
    
    parser = OptionParser(
        usage="usage: %prog [options] input output",
        description="Given a TSV file of searches and URLs (absolute, or relative to the search HTTP endpoint) that should be returned in order of importance, outputs a TSV file indicating the 0-indexed position each URL was found on the first page, plus an 'accuracy' score; prints out the query and accuracy score as it goes. Prints a final summary including the average accuracy score. Errors in testing a query (eg HTTP failures) are treated as all expected matches being missing.",
    )
    parser.add_option("-s", "--selector", dest="selector", help="CSS selector used to find matches", default="ol li a")
    parser.add_option("-e", "--endpoint", dest="endpoint", help="Search HTTP endpoint to test", default="http://localhost:8000/search/")
    parser.add_option("-p", "--query-param", dest="param", help="HTTP query parameter to use", default="q", metavar="PARAM")
    
    (options, args) = parser.parse_args()
    if len(args) != 2:
        parser.error("Must provide both input and output filenames.")
    s = SearchSystemTest(
        endpoint = options.endpoint,
        selector = options.selector,
        param = options.param
    )
    s.test_searches(args[0], args[1])
    return 0


def scoretest():
    from searchtester.scoring import calculate_score
    import csv
    from optparse import OptionParser
    
    parser = OptionParser(
        usage="usage: %prog [options] resultsfile",
        description="Given a TSV file of searches and 0-indexed positions the best matches were found at, print an 'accuracy' score for each query. Prints a final summary including the average accuracy score.",
    )
    
    (options, args) = parser.parse_args()
    if len(args) != 1:
        parser.error("Must provide a results file, from a previous searchtest run .")
    with open(args[0]) as f:
        print "Calculating scores..."
        print
        r = csv.reader(f, dialect='excel-tab')
        scores = []
        for count, row in enumerate(r):
            score = calculate_score(row[2:])
            scores.append(score)
            if len(row[0]) > 69:
                truncated_name = row[0][:69] + u"…"
            else:
                truncated_name = row[0]
            print u"  %-70.70s %.2f" % (truncated_name, score)
            if count % 10 == 9:
                print
                print "Average score", float(sum(scores)) / len(scores)
                print
    print
    print "Summary"
    print "-------"
    print
    print "%i queries, average score %f." % (len(scores), float(sum(scores)) / len(scores))
    print

    return 0
