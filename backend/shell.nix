{pkgs ? import <nixpkgs> {}}:
pkgs.mkShell {
  packages = [
    (pkgs.python311.withPackages (ps: [
      ps.fastapi
      ps.asyncpg
      ps.psycopg2
      ps.sqlalchemy
      ps.uvicorn
      ps.email_validator
    ]))
  ];
}
