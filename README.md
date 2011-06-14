# searchtester

searchtester is a simple way of generating "accuracy" scores for a set
of searches that you care about against ideal results. You can either
use the `searchtest` command to run the queries against a live
endpoint (which is fine for small sets, but can be very slow and
result in high load against your system for large ones), or use
`scoretest` to rank a set of searches against the positions the ideal
results actually appeared. Both produce the same score, using the same
algorithm.

## Running search tests

Given a TSV with each row containing the query to search followed by
as many possible result URLs as you want in the order they should
appear, running a search test can be as simple as:

    searchtest input.tsv output.tsv

However usually you have to change some of the defaults. A more
realistic run would be:

    searchtest -s 'ol.results > li a' -e http://example.com/search/ input.tsv output.tsv

The `-s` option sets a CSS selector to find the anchors for your
search results; the `href` attribute of these will then be compared
with the URLs in your input file. Let's look at what an input file
might contain.

<table>
  <tr>
    <td>searchtester</td>
    <td>/artfinder/searchtester</td>
    <td>/alejandrolujan/SearchTest</td>
  <tr>
</table>

Given this, `searchtest` will run a query for `searchtester`,
expecting to see the two URLs, in that order, in the results; it only
checks the first page of results. Let's run it against github:

    searchtest -s '#code_search_results h2 a' -e https://github.com/search sample.tsv output.tsv

That actually looks pretty bad:

    Running searches...
    
      searchtester                                                           0.00
    
    Summary
    -------
    
    Ran 1 queries in 2.30 seconds, average score 0.004926.

Mostly because (at least right now) there are a bunch of dead projects
and Rails clones cluttering up the results.

The last option you may need is `-p`, which allows you to change the
default query parameter from `q`.

## Running scoring

The output file from `searchtest` can be run into `scoretest` to
regenerate those scores, although that's not terribly useful. What is
useful is that you can generate a file in the same format, which is
pretty simple: each row contains two fixed columns, the query and the
score (ignored by `scoretest`), followed by a column for each expected
result, and where it was actually found in the results. Expected
results that weren't found are stored as blanks.

So we can do:

    scoretest output.tsv

and we get the reassuring:

    Calculating scores...
      searchtester                                                           0.00
    
    Summary
    -------
    
    1 queries, average score 0.004926.

## Caveats

Does not check `robots.txt`, so running this with large search sets
against someone else's site is a bad idea; most likely you'll get your
IP range blocked. Currently we only use it for testing our own
endpoints, so there's no pressure to add this feature, but we'd
welcome a pull request for it.

# Contact

Via [the github project page](http://github.com/artfinder/searchtester).
