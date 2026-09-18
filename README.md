# getparable/homebrew-tap

Homebrew formulae for [getparable](https://github.com/getparable) tools.

```sh
brew install getparable/tap/aiu
```

## aiu

[aiu](https://github.com/getparable/aiu) shows live Claude and Codex usage limits
for every account you hold, in the menu bar and in the terminal, and switches which
account Claude Code or Codex is signed in as.

On Apple Silicon running macOS 26 this pours a prebuilt bottle in a couple of seconds,
with no compiler and no Xcode involved. An Intel Mac has no bottle and builds from
source instead, which needs Xcode 27 (Swift 6.4).

Either way the result carries no quarantine flag, so Gatekeeper never gets in the way.
It is ad-hoc signed rather than notarized.

After installing, link the app where macOS looks for it:

```sh
ln -sfn "$(brew --prefix aiu)/AIU.app" ~/Applications/AIU.app
open ~/Applications/AIU.app
```

## Releasing a new version

The runbook lives with the app, not here: **[aiu → README → Releasing](https://github.com/getparable/aiu#releasing)**.
The order matters — the bottle has to be built and uploaded to the GitHub release
*before* this formula points at it.

Bumping the formula without doing that does not fail. Homebrew falls back to building
from source, so installs still succeed; they just take minutes and need Xcode again.
`scripts/check-formula.py` guards against it, in CI and locally:

```sh
python3 scripts/check-formula.py
```

It fails if a formula's `url` and its bottle's `root_url` name different versions, or if
the bottle they name is not actually downloadable from the release.
