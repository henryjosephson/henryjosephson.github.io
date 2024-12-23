"""converts draft .md files to ready-to-publish .html files"""

import argparse
import logging
import re
from datetime import datetime as dt
from pathlib import Path

import pypandoc
from constants import HTML_TEMPLATE

logging.getLogger("pypandoc").addHandler(logging.NullHandler())


def get_title_from_html(html_body: str) -> str:
    """Gets title from html body

    Args:
        html_body (str): html body

    Returns:
        str: title
    """
    return re.findall(r"<h1.*>(.*)</h1>", html_body)[0].strip()


def main(
    input_path: Path,
    output_path: Path,
    date: dt.date,
    input_format: str = "markdown",
    output_format: str = "html",
):
    """Converts draft .md files to ready-to-publish .html files

    Args:
        input_path (Path): path to input file
        output_path (Path): path to output file
        date (dt.date): the date to include
        input_format (str, optional): input format. Defaults to 'markdown'.
        output_format (str, optional): output format. Defaults to 'html'.
    """
    pypandoc.convert_file(
        source_file=input_path,
        format=input_format,
        to=output_format,
        outputfile=output_path,
        extra_args=["--wrap=none"],
    )

    with Path(output_path).open("r") as f:
        html_body = f.read()

    title = get_title_from_html(html_body)

    with Path(output_path).open("w") as f:
        f.write(
            HTML_TEMPLATE.replace(
                "<!-- title -->",
                title,
            )
            .replace(
                "<!-- date -->",
                date.strftime("%B %d, %Y"),
            )
            .replace(
                "<!-- body text -->",
                html_body,
            ),
        )


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("--input_path", "-i", type=Path)
    parser.add_argument("--output_path", "-o", type=Path, required=False, default=False)
    args = parser.parse_args()

    in_path = Path(args.input_path)

    date = dt.strptime(
        re.findall(r"\d{4}-\d{2}-\d{2}", str(in_path))[0],
        "%Y-%m-%d",
    ).date()

    if not args.output_path:
        if in_path.parent.name == "_md":
            out_path = Path(
                re.sub(
                    r"\d{4}-\d{2}-\d{2}-",
                    "a",
                    str(args.input_path),
                )
                .replace(".md", ".html")
                .replace("/_md", ""),
            )
        else:
            out_path = Path(
                re.sub(
                    r"\d{4}-\d{2}-\d{2}-",
                    "",
                    str(args.input_path),
                ).replace(".md", ".html"),
            )
    else:
        out_path = args.output_path

    main(
        input_path=in_path,
        output_path=out_path,
        date=date,
    )
