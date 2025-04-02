JSON tooltip target test file: tooltips.json

Valid base file link: java.base / java
Valid base file link: java.compiler / java
Broken file link: java.compiler.BROKEN / java
Valid base file with fragment ignored: java.compiler.FRAGMENT / java

docs/

index.html - valid link to page1.html and invalid link to subdir/page2.html
page1.html - valid link to extra.html with a fragment and query to disregard
extra.html - no links
subdir/page3.html - invalid link to nonexistent.html


