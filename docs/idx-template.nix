{ pkgs, ... }: {
  bootstrap = ''    
    mkdir "$out"
    mkdir -p "$out/.idx/"
    cp -rf ${../.idx/dev.nix} "$out/.idx/dev.nix"
    cp -rf ${../core} "$out"
    cp -r ${../fin_data} "$out"
    cp -r ${../routes} "$out"
    cp -r ${../templates} "$out"
    cp ${../main.py} "$out"
    cp ${../devserver.sh} "$out"
    chmod -R +w "$out"
    chmod +rwx "$out/devserver.sh"
  '';
}