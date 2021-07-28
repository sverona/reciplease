let pkgs = import <nixpkgs> {};
in pkgs.mkShell {
	buildInputs = with pkgs.python3Packages; [
    beautifulsoup4
		black
    requests
	];
}
