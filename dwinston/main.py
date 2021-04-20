from typing import Optional

from fastapi import FastAPI, Response, Header, status
from fastapi.responses import HTMLResponse

app = FastAPI()

html_content = """
<html>
  <style type="text/css">
    dt { font-weight: bold; text-decoration: underline dotted; }
  </style>
  <body>
    <dl>
      <dt id="helloWorld">hello world</dt>
      <dd>This is a beatiful term.</dd>
    </dl>
  </body>
</html>
"""

html_content = """
<html>
  <style type="text/css">
    dt { font-weight: bold; text-decoration: underline dotted; }
  </style>
  <body>
    <dl>
      <dt id="helloWorld">hello world</dt>
      <dd>This is a beatiful term.</dd>
    </dl>
  </body>
</html>
"""

turtle_content = """
@base <http://ns.polyneme.xyz/2021/04/marda-dd/test> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
<#helloWorld>
  rdfs:label "hello world" ;
  rdfs:comment "This is a beautiful term." .
"""


def want_rdf(accept: str):
    # e.g. "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8"
    alternatives = [a.split(";") for a in accept.split(",")]
    for a in alternatives:
        if len(a) == 1:
            a.append("q=1")
    alternatives = sorted(
        [(type_, float(qexpr[2:])) for type_, qexpr in alternatives],
        key=lambda a: a[1],
        reverse=True
    )
    types_ = [a[0] for a in alternatives]
    for t in types_:
        if t == "text/html":
            return False
        elif "turtle" in t or "rdf" in t:
            return True
    return False


@app.get("/test")
async def root(response: Response, accept: Optional[str] = Header(None)):
    response.status_code = status.HTTP_303_SEE_OTHER
    if want_rdf(accept):
        return Response(content=turtle_content, media_type="text/turtle")
    else:
        return HTMLResponse(content=html_content, status_code=200)