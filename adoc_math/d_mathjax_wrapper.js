#!/usr/bin/env node

const util = require('util');
const fs = require("fs");
const MJ = require("mathjax");

let mj;

const main = async () => {
    mj = await MJ.init({
        loader: {
            load: [
                'input/tex',
                '[tex]/boldsymbol',
                'output/svg',
                'input/asciimath',
            ]
        },
        tex: {
            packages: {
                '[+]': ['boldsymbol']
            },
        },
    });

    const args = process.argv.slice(2);
    let display;
    if (args[1] === "block") {
        display = true;
    } else if (args[1] === "inline") {
        display = false;
    } else {
        throw Error(`Incorrect value provided for second argument: ${args[1]}`);
    }

    const stdin_buffer = fs.readFileSync(0); // STDIN_FILENO = 0
    const data = stdin_buffer.toString();

    let svg_object_wrapped;
    if (args[0] == "tex") {
        // https://docs.mathjax.org/en/latest/web/typeset.html?highlight=outerhtml#conversion-options
        svg_object_wrapped = mj.tex2svg(data, {
            display,
        });
    } else if (args[0] == "amath") {
        svg_object_wrapped = mj.asciimath2svg(data);
    } else {
        throw Error(`Incorrect value provided for first argument: ${args[0]}`);
    }

    const svg_object = svg_object_wrapped.children[0];
    const svg_html = mj.startup.adaptor.outerHTML(svg_object);

    console.log(svg_html.toString());
}

main().catch (error => {
    console.error(error)
    process.exit(1)
})