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
