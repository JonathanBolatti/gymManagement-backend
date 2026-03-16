#!/usr/bin/env python3
"""Agente de Code Review usando Gemini API + GitHub API."""

import argparse
import json
import os
import sys
import requests
from pathlib import Path
import google.generativeai as genai

REFERENCE_MODULE = "src/main/java/com/gym_management/system/controller/MemberController.java"
CLAUDE_MD        = "CLAUDE.md"
PROMPT_SECTION   = "## Prompt para GitHub Actions"


def load_prompt_template() -> str:
    """Extrae la sección '## Prompt para GitHub Actions' del CLAUDE.md."""
    claude_md = Path(CLAUDE_MD)
    if not claude_md.exists():
        raise FileNotFoundError(f"{CLAUDE_MD} no encontrado. Debe existir en la raíz del repo.")
    content = claude_md.read_text(encoding="utf-8")
    start = content.find(PROMPT_SECTION)
    if start == -1:
        raise ValueError(f"Sección '{PROMPT_SECTION}' no encontrada en {CLAUDE_MD}.")
    # Tomar todo desde después del encabezado de la sección
    return content[start + len(PROMPT_SECTION):].strip()


def get_diff(owner: str, repo: str, pr: int, token: str) -> str:
    url = f"https://api.github.com/repos/{owner}/{repo}/pulls/{pr}"
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github.v3.diff",
    }
    r = requests.get(url, headers=headers, timeout=30)
    r.raise_for_status()
    return r.text


def get_head_sha(owner: str, repo: str, pr: int, token: str) -> str:
    url = f"https://api.github.com/repos/{owner}/{repo}/pulls/{pr}"
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github+json",
    }
    r = requests.get(url, headers=headers, timeout=30)
    r.raise_for_status()
    return r.json()["head"]["sha"]


def call_gemini(prompt: str) -> dict:
    genai.configure(api_key=os.environ["GEMINI_API_KEY"])
    model = genai.GenerativeModel(
        model_name="gemini-2.0-flash",
        generation_config={"response_mime_type": "application/json"},
    )
    response = model.generate_content(prompt)
    return json.loads(response.text)


def post_review(owner: str, repo: str, pr: int, sha: str,
                review: dict, token: str) -> None:
    comments = [
        {
            "path": c["path"],
            "line": c["line"],
            "side": "RIGHT",
            "body": f"**[{c['severity']}] {c['title']}**\n\n{c['body']}",
        }
        for c in review.get("inline_comments", [])
    ]
    summary = review.get("summary", "")
    if not isinstance(summary, str):
        summary = json.dumps(summary, ensure_ascii=False, indent=2)
    payload = {
        "commit_id": sha,
        "body":      summary,
        "event":     "COMMENT",
        "comments":  comments,
    }
    url = f"https://api.github.com/repos/{owner}/{repo}/pulls/{pr}/reviews"
    headers = {
        "Authorization":        f"Bearer {token}",
        "Accept":               "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
    }
    r = requests.post(url, headers=headers, json=payload, timeout=30)
    if not r.ok:
        print(
            f"Warning: review con comentarios falló ({r.status_code}: {r.text}). "
            "Reintentando sin inline...",
            file=sys.stderr,
        )
        payload["comments"] = []
        r = requests.post(url, headers=headers, json=payload, timeout=30)
        r.raise_for_status()


def main():
    parser = argparse.ArgumentParser(
        description="Corre el agente de Code Review con Gemini y postea en GitHub"
    )
    parser.add_argument("--pr",    required=True, type=int, help="Número del PR")
    parser.add_argument("--owner", required=True,           help="Owner del repo")
    parser.add_argument("--repo",  required=True,           help="Nombre del repo")
    args  = parser.parse_args()
    token = os.environ["GITHUB_TOKEN"]

    input_file = Path(f"reviews/pr-{args.pr}-input.md")
    input_md   = input_file.read_text(encoding="utf-8") if input_file.exists() else "(sin input)"

    ref_file       = Path(REFERENCE_MODULE)
    reference_code = ref_file.read_text(encoding="utf-8") if ref_file.exists() else "(no disponible)"

    print(f"→ Obteniendo diff del PR #{args.pr}...")
    diff = get_diff(args.owner, args.repo, args.pr, token)
    sha  = get_head_sha(args.owner, args.repo, args.pr, token)

    print("→ Cargando prompt desde CLAUDE.md...")
    template = load_prompt_template()

    print("→ Llamando a Gemini...")
    prompt = (
        template
        .replace("{input_md}", input_md)
        .replace("{reference_code}", reference_code)
        .replace("{diff}", diff)
        .replace("{pr_number}", str(args.pr))
    )
    print("=" * 60)
    print("PROMPT FINAL ENVIADO A GEMINI:")
    print("=" * 60)
    print(prompt)
    print("=" * 60)
    review_data = call_gemini(prompt)

    print("→ Publicando review en GitHub...")
    post_review(args.owner, args.repo, args.pr, sha, review_data, token)

    out = Path(f"reviews/pr-{args.pr}-gemini-review.json")
    out.write_text(json.dumps(review_data, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"✓ Review publicado. Reporte guardado en {out}")


if __name__ == "__main__":
    sys.exit(main())
