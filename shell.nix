{pkgs ? import <nixpkgs> {}}:
pkgs.mkShell
{
  nativeBuildInputs = with pkgs; [
    ## to locally test actions
    # act
    # docker
    python3
    python3Packages.pip
    python3Packages.pandas
    python3Packages.numpy
  ];

  shellHook = ''
    VENV=.venv
    if test ! -d $VENV; then
      python -m venv $VENV
    fi
    source ./$VENV/bin/activate
  '';
}
