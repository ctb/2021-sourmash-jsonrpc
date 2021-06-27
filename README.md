# a simple sourmash search server, plus client plugin

A simple (and still quite hacky) sourmash client/server search.

See
[sourmash#1484](https://github.com/sourmash-bio/sourmash/issues/1484)
for some info.

## Quickstart

You'll need to have sourmash installed already, using the branch from
[PR #1644](https://github.com/sourmash-bio/sourmash/pull/1644).

Then, run the following.

### Installation:

```
# install necessary packages
pip install jsonrpcserver
pip install "jsonrpcclient[requests]"
```

### Server side:

Start a server on localhost:5000, running in the background:
```
export PYTHONPATH=.
./sourmash-server ./podar-ref/1.sig.gz &
```

### Client side

```
export PYTHONPATH=.
sourmash search ./podar-ref/1.sig.gz http://localhost:5000/
```

and then you should see
```
== This is sourmash version 4.1.3.dev16+g9dbd8b5. ==
== Please cite Brown and Irber (2016), doi:10.21105/joss.00027. ==

selecting specified query k=31
loaded query: CP001941.1 Aciduliprofundum bo... (k=31, DNA)
loaded 1 databases.

1 matches:
similarity   match
----------   -----
100.0%       CP001941.1 Aciduliprofundum boonei T469, complete genome
```

## Notes


### Some details

* Over in
  [PR #1644](https://github.com/sourmash-bio/sourmash/pull/1644), we
  inject a "remote index" loader in sourmash_args. That's what handles the
  http URL on the command line. Ugly, but works for now :).
* The sourmash-server code can serve any sourmash database - so, SBT,
  LCA, pathlist, zipfile, directory, or signature file. Use a pathlist
  if you want to serve multiple indexes as a single database.
  
### Limitations:

* Only the 'find' method works, so 'search' and 'gather' and 'prefetch' but
  not much else.
* Signature retrieval doesn't work, except with search.
* Picklists do not yet work, either.
* One big and invisible gotcha for 'gather' is that the prefetch stage is
  done remotely, and then the gather is done locally. This is straightforward
  to fix.
* Only 50 results are returned at the moment.
