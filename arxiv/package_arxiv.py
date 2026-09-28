#!/usr/bin/env python3
"""
Audits main.tex for arXiv AutoTeX compliance and packages the submission
into both werrsoma_arxiv_package.tar.gz and werrsoma_arxiv_package.zip.
"""
import os
import re
import tarfile
import zipfile

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEX_PATH = os.path.join(BASE_DIR, "main.tex")

REQUIRED_FILES = [
    "main.tex",
    "figures/fig1_werrsoma_architecture.png",
    "figures/fig2_homeostatic_gaba_and_latency.png",
    "figures/fig3_bioenergetics_and_fault_tolerance.png",
]


def audit_latex(tex_path: str) -> None:
    with open(tex_path, "r", encoding="utf-8") as f:
        content = f.read()
    lines = content.splitlines()

    # 1. Check first line for \pdfoutput=1
    assert lines[0].strip() == r"\pdfoutput=1", "First line must be \\pdfoutput=1 for arXiv AutoTeX"

    # 2. Check balanced curly braces (ignoring escaped \{ and \})
    clean = re.sub(r"\\[{}]", "", content)
    # Remove comments
    clean_lines = []
    for line in clean.splitlines():
        # Remove % comments (ignoring \%)
        line_no_comment = re.split(r"(?<!\\)%", line)[0]
        clean_lines.append(line_no_comment)
    clean_text = "\n".join(clean_lines)

    open_braces = clean_text.count("{")
    close_braces = clean_text.count("}")
    assert open_braces == close_braces, f"Unbalanced braces: {{={open_braces}, }}={close_braces}"

    # 3. Check matching \begin{...} and \end{...}
    begins = re.findall(r"\\begin\{([^}]+)\}", clean_text)
    ends = re.findall(r"\\end\{([^}]+)\}", clean_text)
    assert begins == ends or sorted(begins) == sorted(ends), f"Mismatched environments: {begins} vs {ends}"

    stack = []
    for match in re.finditer(r"\\(begin|end)\{([^}]+)\}", clean_text):
        kind, env = match.group(1), match.group(2)
        if kind == "begin":
            stack.append(env)
        else:
            assert stack and stack[-1] == env, f"Unexpected \\end{{{env}}}, stack={stack}"
            stack.pop()
    assert not stack, f"Unclosed environments: {stack}"

    # 4. Check all \includegraphics files exist
    gfx = re.findall(r"\\includegraphics(?:\[[^\]]*\])?\{([^}]+)\}", clean_text)
    for g in gfx:
        full_g = os.path.join(BASE_DIR, g)
        assert os.path.isfile(full_g) and os.path.getsize(full_g) > 10000, f"Missing or empty figure: {g}"

    # 5. Check all \cite{...} keys exist in \bibitem{...}
    bibitems = set(re.findall(r"\\bibitem\{([^}]+)\}", clean_text))
    cite_groups = re.findall(r"\\cite\{([^}]+)\}", clean_text)
    cited_keys = set()
    for group in cite_groups:
        for k in group.split(","):
            cited_keys.add(k.strip())
    missing_cites = cited_keys - bibitems
    assert not missing_cites, f"Missing bibitem definitions for cited keys: {missing_cites}"

    # 6. Check all \ref{...} labels exist in \label{...}
    labels = set(re.findall(r"\\label\{([^}]+)\}", clean_text))
    refs = set(re.findall(r"\\ref\{([^}]+)\}", clean_text))
    missing_refs = refs - labels
    assert not missing_refs, f"Missing label definitions for refs: {missing_refs}"

    # 7. Check for non-ASCII characters that could break pdflatex T1/UTF8
    non_ascii = [(i + 1, ch) for i, line in enumerate(lines) for ch in line if ord(ch) > 127]
    assert not non_ascii, f"Found non-ASCII characters in main.tex: {non_ascii[:5]}"

    print("[OK] LaTeX audit passed:")
    print(f"     - Line 1: {lines[0].strip()}")
    print(f"     - Braces balanced: {open_braces} open / {close_braces} close")
    print(f"     - Environments matched: {len(begins)} pairs")
    print(f"     - Figures verified: {gfx}")
    print(f"     - Citations verified: {len(cited_keys)}/{len(bibitems)} keys")
    print(f"     - Cross-references verified: {sorted(refs)}")
    print("     - Pure 7-bit ASCII LaTeX encoding: 100% compliant")


def build_archives() -> None:
    for rel_path in REQUIRED_FILES:
        abs_path = os.path.join(BASE_DIR, rel_path)
        assert os.path.isfile(abs_path), f"Missing required file: {rel_path}"

    tar_path = os.path.join(BASE_DIR, "werrsoma_arxiv_package.tar.gz")
    with tarfile.open(tar_path, "w:gz") as tar:
        for rel_path in REQUIRED_FILES:
            abs_path = os.path.join(BASE_DIR, rel_path)
            tar.add(abs_path, arcname=rel_path)

    zip_path = os.path.join(BASE_DIR, "werrsoma_arxiv_package.zip")
    with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        for rel_path in REQUIRED_FILES:
            abs_path = os.path.join(BASE_DIR, rel_path)
            zf.write(abs_path, arcname=rel_path)

    print(f"[OK] Built {tar_path} ({os.path.getsize(tar_path):,} bytes)")
    print(f"[OK] Built {zip_path} ({os.path.getsize(zip_path):,} bytes)")


if __name__ == "__main__":
    audit_latex(TEX_PATH)
    build_archives()
