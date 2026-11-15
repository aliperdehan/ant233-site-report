#!/usr/bin/env bash
# Rebuild submission.pdf: render the three documents with pdfmd, then merge
# them (site report, AI-use acknowledgement, annotated bibliography) with qpdf.
# Run from anywhere: ./build.sh
set -euo pipefail

cd "$(dirname "${BASH_SOURCE[0]}")"

docs=(SR/SR.md SR/AI-use.md AB-new/ab_new.md)
pdfs=()

for md in "${docs[@]}"; do
  extra=()
  # AI-use.md has no citations. pdfmd >= 3.33.216 still turns citeproc on for
  # it because metadata.yaml names a CSL, and the build then fails with
  # "File '' not found in resource path"; --no-citeproc sidesteps that.
  [[ $md == SR/AI-use.md ]] && extra=(--no-citeproc)
  echo "== pdfmd $md ${extra[*]}"
  pdfmd "$md" "${extra[@]}"
  pdfs+=("${md%.md}.pdf")
done

echo "== qpdf -> submission.pdf"
qpdf --empty --pages "${pdfs[@]}" -- submission.pdf

echo "== check"
qpdf --check submission.pdf 2>&1 | tail -1
pdfinfo submission.pdf | grep -E 'Pages|File size'
