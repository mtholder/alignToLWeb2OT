# alignToLWeb2OT

This repo has the beginnings of scripts for aligning the Tree of Life web project's
tree to the taxonomy used by the Open Tree of Life project.

## Background

### Tree of Life Web project
The [Tree of Life web project](http://tolweb.org) is a fantastic resource containing a wealth of
information about the phylogeny of life on Earth and summaries of many aspects
of the biology for many clades. The "taxon pages" for the project are written by a
large community of
[professional biologists and non-professional natural historians](http://tolweb.org/onlinecontributors/app?page=PeopleList&service=external&sp=1)
and these pages represent a remarkably successful example of a community project
that engages both scientists and the public.
The entire site provides a rich educational and research tool, and the project
also features ["treehouse pages"](http://tolweb.org/tree/home.pages/treehouses.html)
to provide additional educational resources.


### Open Tree of Life
The [Open Tree of Life project](http://blog.opentreeoflife.org/)
is trying to piece together what is known about the
phylogenetic relationships of Life on Earth using software tools for
automatically merging phylogenetic statements as well feedback from the community
of systematic biologists.

# Goals of this repo
We would like to be able to automatically align the tree structure of the ToLWeb
project to the reference taxonomy used by the Open Tree project.
This would make it easy to provide links to TolWeb pages when such pages are
available.
Note that browsing the Open Tree of Life's tree
already shows links to NCBI, GBIF, and other taxonomic resources
for tips e.g (http://tree.opentreeoflife.org/opentree/argus/ottol@770315/Homo-sapiens)
and internal node e.g. (http://tree.opentreeoflife.org/opentree/otol.draft.22@3061935/Homininae)

# history of this repo

For the sake of convenience, the ToLWeb tree structure was converted to JSON.

   1. The download of the XML was done on 28 Nov, 2014 using methods described on 
[the ToLWeb webservices page](http://tolweb.org/tree/home.pages/downloadtree.html).
See archived/grab_root.py for the script used. Note that the tree structure of the ToLWeb
project is licensed under the [Creative Commons Attribution 3.0](http://creativecommons.org/licenses/by/3.0/)
license. That applies to the modified version of the export which is the `tolweb.json` file
in this repo. All code in this repo is free under a BSD-style license; see License.txt Also note
that the ToLWeb webservices page points out that other content on the ToLWeb site may be licensed
under other terms. See (http://tolweb.org/tree/home.pages/tolcopyright.html)

   2. The conversion to JSON was done with the `archived/convert_tolweb_to_json.py` file. See the
`rename` dict in that file for the conversion rules from the XML elements and attributes to more JSON-like
names (camelCase).

   3. `tolweb.json` is the output. Normally it is not a great idea to store outputs in version control,
doing so in this case will allow us to avoid over-taxing the ToLWeb servers.

   4. `tolweb.py` is under active development. It attempts to provide a pythonic read-only interface
to the JSON dump of TolWeb.

# current functionality

(as of 1 Dec, 2014). Currently the script relies on the (unstable) `ott` branch of [peyotl](https://github.com/OpenTreeOfLife/peyotl)
with peyotl configured to use OTT 2.8 or 2.9 in its OTT wrapper.


As a first step in alignment, the script currently looks for names which are in OTT and which are not
(as far as the reference taxonomy knows) homonyms.

When executed, the script checks each of the names for tips in ToLWeb against OTT, and notes whether
the name is 1. does not exist in OTT (no fuzzy matching is used), 2. is a known homonym in OTT, or 3. maps to a name
that is not a homonym. An examle of the output is posted at (http://phylo.bio.ku.edu/ot/tolweb2ot-name-mapping.txt).
When run against a (still work in progress) 2.9 version of OTT: 60,443 names map to non-homonyms, 15,339 names are 
not found, and 941 names are ambiguous because they are homonyms.






