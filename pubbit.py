#!/usr/bin/env python3

import os
import sys
import uuid
import shutil
import zipfile
from pathlib import Path
import markdown
from jinja2 import Environment, FileSystemLoader

TEMPLATE_DIR = Path(__file__).parent / "templates"

env = Environment(loader=FileSystemLoader(TEMPLATE_DIR))
env.globals['enumerate'] = enumerate

def get_markdown_files(directory):
	return sorted(Path(directory).rglob("*.md"))

def md_to_html(md_path):
	with open(md_path, "r", encoding="utf-8") as f:
		return markdown.markdown(f.read(), extensions=["fenced_code", "toc"])

def create_epub_structure(base_dir):
	(base_dir / "META-INF").mkdir(parents=True, exist_ok=True)
	(base_dir / "OEBPS").mkdir(exist_ok=True)

	# mimetype file
	with open(base_dir / "mimetype", "w", encoding="utf-8") as f:
		f.write("application/epub+zip")

	# container.xml
	container_xml = """<?xml version="1.0"?>
<container version="1.0"
		   xmlns="urn:oasis:names:tc:opendocument:xmlns:container">
  <rootfiles>
	<rootfile full-path="OEBPS/content.opf"
			  media-type="application/oebps-package+xml"/>
  </rootfiles>
</container>
"""
	with open(base_dir / "META-INF" / "container.xml", "w", encoding="utf-8") as f:
		f.write(container_xml)

def render_template(name, **kwargs):
	return env.get_template(name).render(**kwargs)

def create_epub_from_markdown(md_files, output_filename="output.epub", title="Collected Markdown", author="Markdown Compiler"):
	temp_dir = Path("temp_epub")
	create_epub_structure(temp_dir)
	oebps_dir = temp_dir / "OEBPS"

	uid = str(uuid.uuid4())
	chapter_titles = []
	for i, md_file in enumerate(md_files):
		chapter_title = md_file.stem
		chapter_titles.append(chapter_title)
		html = md_to_html(md_file)
		chapter_content = render_template("chapter.xhtml.j2", title=chapter_title, content=html)
		with open(oebps_dir / f"chap{i}.xhtml", "w", encoding="utf-8") as f:
			f.write(chapter_content)

	# Write OPF
	content_opf = render_template(
		"content.opf.j2",
		title=title,
		uid=uid,
		author=author,
		chapter_count=len(md_files)
	)
	with open(oebps_dir / "content.opf", "w", encoding="utf-8") as f:
		f.write(content_opf)

	# Write NCX
	toc_ncx = render_template(
		"toc.ncx.j2",
		uid=uid,
		title=title,
		chapter_titles=chapter_titles
	)
	with open(oebps_dir / "toc.ncx", "w", encoding="utf-8") as f:
		f.write(toc_ncx)

	# Create EPUB zip
	with zipfile.ZipFile(output_filename, "w") as epub:
		epub.write(temp_dir / "mimetype", "mimetype", compress_type=zipfile.ZIP_STORED)
		for root, _, files in os.walk(temp_dir):
			for file in files:
				if file == "mimetype":
					continue
				full_path = Path(root) / file
				rel_path = full_path.relative_to(temp_dir)
				epub.write(full_path, str(rel_path), compress_type=zipfile.ZIP_DEFLATED)

	shutil.rmtree(temp_dir)
	print(f"EPUB created: {Path(output_filename).resolve()}")


def main():
	if len(sys.argv) < 2:
		print("Usage: python make_epub.py <markdown-directory>")
		sys.exit(1)

	md_dir = Path(sys.argv[1])
	if not md_dir.is_dir():
		print(f"Invalid directory: {md_dir}")
		sys.exit(1)

	md_files = get_markdown_files(md_dir)
	if not md_files:
		print("No markdown files found.")
		sys.exit(1)

	create_epub_from_markdown(md_files)


if __name__ == '__main__':
	main()
