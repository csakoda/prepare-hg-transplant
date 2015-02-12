# Purpose

This script prepares an `hg transplant` from an existing branch, (optionally) filtering out all the commits that are merges, outputing the `hg` command that should be run

# A Stern Warning

Blindly filtering merging commits is *probably not wise* overall, and is a strong indicator that something is fundamentally broken in your merge workflow.  

But in times of desperate need...this should reduce some bleeding (mostly when you started work on `trunk` but need to promote to `main` without including other changesets from `trunk`)

# Usage

```
python prepare.py REPOPATH BRANCH'
```
* `REPOPATH` - Local path to repo
* `BRANCH` - Branch to transplant changes from

This will output a sample `hg transplant` command for you to apply to a new branch at a proper merge point, e.g.

```
hg update main
hg branch new-branch-rebased-to-main
<hg transplant command from output above>
```
