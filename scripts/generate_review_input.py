#!/usr/bin/env python3
"""Genera reviews/pr-N-input.md a partir de los datos de un PR de GitHub."""

import argparse
import re
import sys
from pathlib import Path

CHANGE_TYPE_RULES = [
    (r"controller",                     "Feature — nuevo endpoint / controller"),
    (r"service",                        "Feature — lógica de negocio / service"),
    (r"repository",                     "Feature — acceso a datos / repository"),
    (r"model|dto|entity",               "Feature — modelo de datos"),
    (r"security|auth|jwt",              "Seguridad — autenticación / autorización"),
    (r"test",                           "Tests — cobertura / unit / integration"),
    (r"config",                         "Configuración — infraestructura / setup"),
    (r"migration|sql|flyway|liquibase", "Base de datos — migración / schema"),
]


def detect_change_type(branch: str, title: str) -> str:
    text = f"{branch} {title}".lower()
    for pattern, label in CHANGE_TYPE_RULES:
        if re.search(pattern, text):
            return label
    return "Cambio general"


def extract_checkboxes(body: str) -> list[str]:
    return re.findall(r"-\s*\[[ xX]\]\s*(.+)", body)


def generate_input_md(pr: int, branch: str, base: str, title: str, body: str) -> str:
    change_type = detect_change_type(branch, title)
    checkboxes  = extract_checkboxes(body)

    dod_section = "\n".join(f"- [ ] {item}" for item in checkboxes) if checkboxes else ""

    return f"""# PR #{pr} — {title}

## Origen (output del Agente de Desarrollo)
- Tarea: generado automáticamente via webhook
- Rama origen: {branch}
- Rama destino: {base}
- Tipo de cambio: {change_type}

## PRD
{body.strip() if body.strip() else "(sin descripción)"}

## Definition of Done
{dod_section}

## Notas para el Agente de Code Review
Generado automáticamente por GitHub Actions. Revisar PRD para contexto adicional.
"""


def main():
    parser = argparse.ArgumentParser(
        description="Genera pr-N-input.md para el agente de Code Review"
    )
    parser.add_argument("--pr",     required=True, type=int, help="Número del PR")
    parser.add_argument("--branch", required=True,           help="Rama origen")
    parser.add_argument("--base",   required=True,           help="Rama destino")
    parser.add_argument("--title",  required=True,           help="Título del PR")
    parser.add_argument("--body",   default="",              help="Descripción del PR")
    args = parser.parse_args()

    output_dir  = Path("reviews")
    output_dir.mkdir(exist_ok=True)
    output_file = output_dir / f"pr-{args.pr}-input.md"

    content = generate_input_md(args.pr, args.branch, args.base, args.title, args.body)
    output_file.write_text(content, encoding="utf-8")

    print(f"✓ Generado: {output_file}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
