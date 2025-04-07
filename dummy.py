#!/usr/bin/env python3

import os
import random
import argparse
from pathlib import Path

LOREM = [
	"Lorem ipsum dolor sit amet, consectetur adipiscing elit.",
	"Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.",
	"Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris.",
	"Duis aute irure dolor in reprehenderit in voluptate velit esse cillum.",
	"Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia.",
	"Curabitur pretium tincidunt lacus. Nulla gravida orci a odio.",
	"Nullam varius, turpis et commodo pharetra, est eros bibendum elit.",
	"Praesent dapibus, neque id cursus faucibus, tortor neque egestas auguae.",
	"Morbi interdum mollis sapien. Sed ac risus. Phasellus lacinia, magna a ullamcorper.",
	"Fusce suscipit varius mi. Cum sociis natoque penatibus et magnis dis parturient."
]

def generate_random_paragraph(lines=5):
	return " ".join(random.choice(LOREM) for _ in range(lines))

def generate_paragraphs(num=3):
	paragraphs = []
	for i in range(num):
		lines = random.randint(1, 10)
		paragraph = generate_random_paragraph(lines)
		paragraphs.append(paragraph)
	return "\n\n".join(paragraphs)

def generate_sample_md_dir(dirname: str, number_of_chapters: int):
	base = Path(dirname)
	base.mkdir(parents=True, exist_ok=True)

	for i in range(1, number_of_chapters + 1):
		chapter_title = f"Chapter {i}"
		filename = base / f"{i:02d}_{chapter_title.replace(' ', '_').lower()}.md"
		para_count = random.randint(50, 200)
		content = f"# {chapter_title}\n\n{generate_paragraphs(para_count)}\n"
		with open(filename, "w", encoding="utf-8") as f:
			f.write(content)

	print(f"Generated {number_of_chapters} markdown files in: {base.resolve()}")


def main():
	parser = argparse.ArgumentParser(description="Generate dummy markdown files.")
	parser.add_argument("--dirname", type=str, default="dummy", help="Target directory name")
	parser.add_argument("--chapters", type=int, default=10, help="Number of chapters to generate")
	args = parser.parse_args()

	generate_sample_md_dir(args.dirname, args.chapters)


if __name__ == "__main__":
	main()
