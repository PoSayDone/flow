{pkgs ? import <nixpkgs> {}}:
pkgs.mkShell {
  packages = [
    (pkgs.python311.withPackages (ps: [
      ps.fastapi
      ps.pip
      ps.asyncpg
      ps.psycopg2
      ps.sqlalchemy
      ps.uvicorn
      ps.email_validator
      ps.python-jose
      ps.passlib
      ps.python-multipart
    ]))
  ];
}
