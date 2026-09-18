# getparable/homebrew-tap

Homebrew formulae for [getparable](https://github.com/getparable) tools.

```sh
brew install getparable/tap/aiu
```

## aiu

[aiu](https://github.com/getparable/aiu) shows live Claude and Codex usage limits
for every account you hold, in the menu bar and in the terminal, and switches which
account Claude Code or Codex is signed in as.

The formula **builds from source**: it needs Xcode 26 and macOS 26, and compiles
both the Go CLI and the SwiftUI menu bar app. Because Homebrew builds it on your own
machine, the result carries no quarantine flag and Gatekeeper never gets in the way —
but it is not a notarized build either. The app that runs is the one brew just built.

After installing, link the app where macOS looks for it:

```sh
ln -sfn "$(brew --prefix aiu)/AIU.app" ~/Applications/AIU.app
open ~/Applications/AIU.app
```
