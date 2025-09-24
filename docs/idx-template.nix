{ pkgs, ... }: {
  packages = [
    pkgs.python3
    pkgs.python312Packages.pip
    pkgs.python312Packages.fastapi
    pkgs.python312Packages.uvicorn
    pkgs.uv
  ];
  bootstrap = ''    
    mkdir "$out"
    mkdir -p "$out/.idx/"
    cp -rf ${../.idx/dev.nix} "$out/.idx/dev.nix"
    shopt -s dotglob; cp -r ${../core}/* "$out"
    cp -r ${../fin_data}/* "$out"
    cp -r ${../routes}/* "$out"
    cp -r ${../templates}/* "$out"
    cp ${../main.py} "$out"
    chmod -R +w "$out"
    chmod +rwx "$out/devserver.sh"
  '';
}