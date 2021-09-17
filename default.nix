with import <nixpkgs> {};
with pkgs.python3Packages;

let pytest-pspec = buildPythonPackage rec {
  pname = "pytest-pspec";
  version = "0.0.4";
  propagatedBuildInputs = [ numpy six pytest ];
  src = fetchPypi {
    inherit pname version;
    sha256 = "0yp6pxjxygsm2i8dfkwcynxklcfid8linbiabz66cl2djsg0q2sw";
  };
};
in mkShell {
	buildInputs = [
    beautifulsoup4
		black
    flask
    requests
    pytest
    pytest-pspec
	];
}
