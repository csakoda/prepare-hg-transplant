#!/usr/bin/python
#
# The purpose of this script is to prepare a 'hg transplant' from an existing branch, 
# filtering out all the merging commits
#
# Blindly filtering merging commits is probably not wise overall, but in times of desperate
# need... (mostly when you started work on trunk but need to promote to main without including 
# other changesets from trunk)
#

import hglib
import sys

if len(sys.argv) != 3:
    print 'Usage: ./prepare.py REPOPATH BRANCH'
    exit(1)

client = hglib.open(sys.argv[1])
branch = sys.argv[2]

def _get_commits(branch, onlymerges=False):
    '''Return the hash and commit message of branches as a list, newest to oldest
    '''
    return [ { 'hash': commit[1], 'msg': commit[5] } for commit in client.log(branch=branch, onlymerges=onlymerges) ]

commits = _get_commits(branch)
merges = _get_commits(branch, onlymerges=True)

print 'Inspecting branch {0}'.format(branch)
print 'Found {0} total commits'.format(len(commits))
print 'Found {0} merges to potentially ignore during transplant (ordered from oldest to newest)'.format(len(merges), branch)

include_txt = 'Include merge? [N/y] '
transplants = []
for c in reversed(commits):
    if c in merges:
        print '{0}: {1}'.format(c['hash'], c['msg'])
        include = raw_input(include_txt)
        while include.lower() not in [ 'y', 'n', '' ]:
            include = raw_input(include_txt)
        if not include:
            include = 'n'
        if include == 'n':
            print 'Not transplanting merge changeset {0}'.format(c['hash'])
        else:
            transplants.append(c)
    else:
        print 'Transplanting changeset {0}: {1}'.format(c['hash'], c['msg'])
        transplants.append(c)
print
print '====='
print
print 'Selected {0} changesets to transplant'.format(len(transplants))

print 'To transplant the selected changes, you could try (on a new branch from the correct branch point):'
print
print 'hg transplant {0}'.format(' '.join([t['hash'] for t in transplants]))

