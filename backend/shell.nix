{pkgs ? import <nixpkgs> {}}: let
  fastapi-socketio = let
    pname = "fastapi-socketio";
    version = "0.0.10";
  in
    pkgs.python311Packages.buildPythonPackage {
      inherit pname version;
      src = pkgs.fetchPypi {
        inherit pname version;
        sha256 = "sha256-IC+bMZ8BAAHL0RFOySoNnrX1ypMW6uX9QaYIjaCBJyc=";
      };
      doCheck = false;
    };
  pusher = let
    pname = "pusher";
    version = "3.3.2";
  in
    pkgs.python311Packages.buildPythonPackage {
      inherit pname version;
      src = pkgs.fetchPypi {
        inherit pname version;
        sha256 = "sha256-FPQSyOJlYqr2Y6EUlReS/vrgHw0iDayElx+SZARiB2A=";
      };
      doCheck = false;
    };
in
  pkgs.mkShell {
    packages = [
      (pkgs.python311.withPackages (ps: [
        fastapi-socketio
        pusher
        ps.fastapi
        ps.pip
        ps.asyncpg
        ps.psycopg2
        ps.sqlalchemy
        ps.uvicorn
        ps.email_validator
        ps.python-jose
        ps.passlib
        ps.pillow
        ps.python-multipart
      ]))
    ];
  }
