class Aiu < Formula
  desc "Live Claude and Codex usage limits for every account you hold"
  homepage "https://github.com/getparable/aiu"
  url "https://github.com/getparable/aiu/archive/refs/tags/v0.1.2.tar.gz"
  sha256 "5940263c10c57ee40a61cab5c1194669c561de8c1fb35286df6ca8f5a62f5d3b"
  license "MIT"
  head "https://github.com/getparable/aiu.git", branch: "main"

  depends_on "go" => :build
  depends_on xcode: ["27.0", :build]
  depends_on macos: :tahoe

  # The CLI and the menu bar app are one build on purpose: `aiu` in the Cellar is a
  # symlink to the binary inside the app bundle, so the two can never drift apart.
  def install
    system "make", "app", "VERSION=#{version}"
    prefix.install "build/AIU.app"
    bin.install_symlink prefix/"AIU.app/Contents/MacOS/aiu"
  end

  def caveats
    <<~EOS
      `aiu` is on your PATH now. The menu bar app is at:

        #{opt_prefix}/AIU.app

      Link it where macOS looks for apps, so Launch at Login and Spotlight find it:

        ln -sfn #{opt_prefix}/AIU.app ~/Applications/AIU.app
        open ~/Applications/AIU.app

      That path stays valid across upgrades, so the link survives `brew upgrade aiu`.

      aiu keeps its own copy of each login in the keychain and rewrites Claude Code's
      or Codex's credentials when you switch. It reads each account at most once
      every 5 minutes, shared between the app and the terminal.
    EOS
  end

  test do
    assert_match "aiu #{version}", shell_output("#{bin}/aiu --version")
    assert_match "rate limits and reset times", shell_output("#{bin}/aiu --help")

    # No accounts tracked in the sandbox, so this exercises argument handling and
    # the JSON encoder without reaching the network or the keychain.
    assert_equal "[]", shell_output("#{bin}/aiu status --json --no-sync").strip
  end
end
