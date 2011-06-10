import csv
import urllib
import urlparse
import sys
from lxml.html import parse
import eventlet
from eventlet.green import urllib2

from searchtester.scoring import calculate_score

class SearchSystemTest(object):

    def __init__(self, endpoint, selector='ol li a', param='q', extra={}):
        self.endpoint = endpoint
        self.selector = selector
        self.param = param
        self.params = extra

    def make_url(self, query):
        params = {
            self.param: query.encode('utf-8'),
        }
        params.update(self.params)

        url = "%s?%s" % (
            self.endpoint,
            urllib.urlencode(params),
        )
        #print url
        return url

    def test_search(self, query, expected):
        """
        Takes a query string and a list of expected result URLs.
        Returns the number of each URL if on the first result
        page, or None in a position if not present.
        """
        #print expected, query
        url = self.make_url(query)
        # apply base of the search URL endpoint
        expected = map(lambda x: urlparse.urljoin(url, x), expected)
        f = urllib2.urlopen(url)
        root = parse(f).getroot()
        f.close()
        #print root
        
        positions = {} # index in expected list
        for i, link in enumerate(root.cssselect(self.selector)):
            actual = link.get("href")
            resolved = urlparse.urljoin(url, actual)
            for idx, possible in enumerate(expected):
                # print i, idx, actual, resolved, possible
                if resolved == possible and positions.get(idx, None) is None:
                    positions[idx] = i
        result = []
        for i in range(0, len(expected)):
            result.append(positions.get(i, None))
        return result

    def test_searches(self, in_filename, out_filename, poolsize=10):
        """
        Takes a file where each line gives a search and a list of
        expected URLs.
        """
        pool = eventlet.GreenPool(size=poolsize)

        inf = open(in_filename, 'r')
        r = csv.reader(inf, dialect='excel-tab')
        def doeeet(row):
            row = map(
                lambda x: x.strip(),
                map(
                    lambda x: x.decode('utf-8'),
                    row
                )
            )
            query = row[0]
            expected = row[1:]
            try:
                return (query, self.test_search(query, expected))
            except:
                print >>sys.stderr, "Caught exception while testing", query.encode('utf-8')
                return (query, map(lambda x: None, expected))
        results = pool.imap(doeeet, r)
        with open(out_filename, 'w') as outf:
            w = csv.writer(outf, dialect='excel-tab')
            scores = []
            for count, result in enumerate(results):
                score = calculate_score(result[1])
                scores.append(score)
                row = [ result[0], score ] # the query and score
                row.extend(result[1]) # and the positions
                w.writerow(map(lambda x: unicode(x).encode('utf-8') if x is not None else "", row))
                print "\t%s\t%s" % (result[0], score)
                if count % 10 == 9:
                    print "Average score", float(sum(scores)) / len(scores)
        inf.close()
        print
        print "Summary"
        print "-------"
        print
        print "Ran %i queries, average score %f" % (len(scores), float(sum(scores)) / len(scores))
