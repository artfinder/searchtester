# -*- encoding: utf-8 -*-
import csv
import urllib
import urlparse
import sys
import time
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
        endpoint = list(urlparse.urlparse(self.endpoint))
        existing = urlparse.parse_qs(endpoint[4])
        params.update(existing)
        endpoint[4] = urllib.urlencode(params, True)
        url = urlparse.urlunparse(endpoint)
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
                
                # note that we could just do:
                # if resolved == possible and positions.get(idx, None) is None:
                # but we don't so that duplicate search results get spotted.
                if resolved == possible:
                    if positions.get(idx, None) is not None:
                        # print "found", possible, "already at", positions[idx]
                        del positions[idx]
                    else:
                        # print "found", possible, "at", i
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
        start_time = time.time()
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
        print "Running searches..."
        print
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
                if len(result[0]) > 69:
                    truncated_name = result[0][:69] + "…"
                else:
                    truncated_name = result[0]
                print u"  %-70.70s %.2f" % (truncated_name, score)
                if count % 10 == 9:
                    print
                    print "Average score", float(sum(scores)) / len(scores)
                    print
        inf.close()
        print
        print "Summary"
        print "-------"
        print
        run_time = time.time() - start_time
        print "Ran %i queries in %.2f seconds, average score %f." % (len(scores), run_time, float(sum(scores)) / len(scores))
        print
