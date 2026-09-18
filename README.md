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
