let
    nixpkgs = fetchTarball "https://github.com/NixOS/nixpkgs/tarball/nixos-23.11";
    pkgs = import nixpkgs { config = {}; overlays = []; };
in

pkgs.mkShellNoCC {
    packages = with pkgs; [
        hello
        python311Packages.spotipy
        python311Packages.python-dotenv
        python311Packages.pandas
        python311Packages.streamlit
        python311Packages.plotly
    ];

    shellHook = ''
        hello
    '';
}