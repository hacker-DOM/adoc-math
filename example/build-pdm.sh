cp ./pre.adoc ./post.adoc && \
pdm run adoc-math \
    ./post.adoc  && \
\
asciidoctor-pdf \
    -r asciidoctor-mathematical \
    -o adoc-math-example.pdf \
    ./post.adoc && \
\
open ./adoc-math-example.pdf
