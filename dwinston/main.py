from typing import Optional, Union
from pathlib import Path

from fastapi import FastAPI, Response, Header, HTTPException
from fastapi.responses import HTMLResponse
import rdflib

app = FastAPI()

RDF_BASE = "http://www.w3.org/2000/01/rdf-schema"
TEST_BASE = "http://ns.polyneme.xyz/2021/04/marda-dd/test"


def load_ttl(filename: Union[Path, str]) -> rdflib.Graph:
    g = rdflib.Graph()
    g.parse(str(filename), format="turtle")
    return g


TERMS = load_ttl("./hello_world.ttl")


def render_html(g: rdflib.Graph) -> str:
    header = """<html>
  <style type="text/css">
    dt { font-weight: bold; text-decoration: underline dotted; }
  </style>
  <body>
    <dl>
"""
    footer = """
    </dl>
  </body>
</html>"""

    dl = ""
    _parsed_subjects = set()
    for subject in g.subjects():
        if subject in _parsed_subjects:
            continue
        _parsed_subjects.add(subject)
        term = subject.split(TEST_BASE + "#")[-1]
        label = g.label(subject)
        comment = g.value(
            subject=subject, predicate=rdflib.term.URIRef(f"{RDF_BASE}#comment")
        )

        dt = f"""      <dt id="#{term}">{label}</dt>
      <dd>{comment}</dd>"""
        dl += dt

    return header + dl + footer


def want_rdf(accept: str) -> bool:
    # e.g. "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8"
    alternatives = [a.split(";") for a in accept.split(",")]
    for a in alternatives:
        if len(a) == 1:
            a.append("q=1")
    alternatives = sorted(
        [(type_, float(qexpr[2:])) for type_, qexpr in alternatives],
        key=lambda a: a[1],
        reverse=True,
    )
    types_ = [a[0] for a in alternatives]
    for t in types_:
        if t == "text/html":
            return False
    return True


@app.get("/2021/04/marda-dd/test")
async def root(accept: Optional[str] = Header(None)):
    if want_rdf(accept):
        try:
            return Response(
                content=TERMS.serialize(
                    base=TEST_BASE, encoding="utf-8", format=accept
                ).decode("utf-8"),
                media_type=accept,
            )
        except rdflib.plugin.PluginException as exc:
            raise HTTPException(
                status_code=400,
                detail=f"""Unsupported RDF type: {accept!r}.
Full rdflib traceback:
{exc}""",
            )

    else:
        html_content = render_html(TERMS)
        return HTMLResponse(content=html_content, status_code=200)
