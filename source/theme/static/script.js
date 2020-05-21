'use strict';

/*
 * Functions and event handlers that implement click-to-copy functionality
 * in Sphinx code-blocks on pages.
 */

/*
 * Adapted Font Awesome icons, CC BY 4.0 License:
 * https://fontawesome.com
 * https://creativecommons.org/licenses/by/4.0/
 */


function nxt_page_load() {
    const template = document.createElement('template');

    /*
    <label class="nxt_copy_btn">
        <input type="radio" name="nxt_copy" onclick="nxt_copy(this)">
        <a title="Click to copy">
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 448 512"><path d="M320 448v40c0 13.255-10.745 24-24 24H24c-13.255 0-24-10.745-24-24V120c0-13.255 10.745-24 24-24h72v296c0 30.879 25.121 56 56 56h168zm0-344V0H152c-13.255 0-24 10.745-24 24v368c0 13.255 10.745 24 24 24h272c13.255 0 24-10.745 24-24V128H344c-13.2 0-24-10.8-24-24zm120.971-31.029L375.029 7.029A24 24 0 0 0 358.059 0H352v96h96v-6.059a24 24 0 0 0-7.029-16.97z" /></svg>
        </a>
        <a title="Copied to clipboard">
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 384 512"><path d="M336 64h-80c0-35.3-28.7-64-64-64s-64 28.7-64 64H48C21.5 64 0 85.5 0 112v352c0 26.5 21.5 48 48 48h288c26.5 0 48-21.5 48-48V112c0-26.5-21.5-48-48-48zM192 40c13.3 0 24 10.7 24 24s-10.7 24-24 24-24-10.7-24-24 10.7-24 24-24zm121.2 231.8l-143 141.8c-4.7 4.7-12.3 4.6-17-.1l-82.6-83.3c-4.7-4.7-4.6-12.3.1-17L99.1 285c4.7-4.7 12.3-4.6 17 .1l46 46.4 106-105.2c4.7-4.7 12.3-4.6 17 .1l28.2 28.4c4.7 4.8 4.6 12.3-.1 17z" /></svg>
        </a>
    </label>
    */

    /* Minified version of the above code. */
    template.innerHTML = '<label class=nxt_copy_btn><input type=radio name=nxt_copy onclick=nxt_copy(this)><a title="Click to copy"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 448 512"><path d="M320 448v40c0 13.255-10.745 24-24 24H24c-13.255.0-24-10.745-24-24V120c0-13.255 10.745-24 24-24h72v296c0 30.879 25.121 56 56 56h168zm0-344V0H152c-13.255.0-24 10.745-24 24v368c0 13.255 10.745 24 24 24h272c13.255.0 24-10.745 24-24V128H344c-13.2.0-24-10.8-24-24zm120.971-31.029L375.029 7.029A24 24 0 00358.059.0H352v96h96v-6.059a24 24 0 00-7.029-16.97z"/></svg></a><a title="Copied to clipboard"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 384 512"><path d="M336 64h-80c0-35.3-28.7-64-64-64s-64 28.7-64 64H48C21.5 64 0 85.5.0 112v352c0 26.5 21.5 48 48 48h288c26.5.0 48-21.5 48-48V112c0-26.5-21.5-48-48-48zM192 40c13.3.0 24 10.7 24 24s-10.7 24-24 24-24-10.7-24-24 10.7-24 24-24zm121.2 231.8-143 141.8c-4.7 4.7-12.3 4.6-17-.1l-82.6-83.3c-4.7-4.7-4.6-12.3.1-17L99.1 285c4.7-4.7 12.3-4.6 17 .1l46 46.4 106-105.2c4.7-4.7 12.3-4.6 17 .1l28.2 28.4c4.7 4.8 4.6 12.3-.1 17z"/></svg></a></label>';

    const btn = template.content.childNodes[0];

    for (let el of document.getElementsByClassName("highlight")) {
        const pre = el.firstChild;
        const html = pre.innerHTML
        const pos = html.indexOf('\n')

        pre.innerHTML = html.slice(0, pos)
                        + '<span class="nxt_copy_ws">     </span>'
                        + html.slice(pos)

        el.parentElement.appendChild(btn.cloneNode(true))
    }

    document.body.addEventListener("copy", function () {
        const el = document.querySelector(".nxt_copy_btn input:checked")
        if (el) {
            el.checked = false
        }
    })
}


function nxt_copy(btn) {
    const container = btn.closest('div')
    let text = container.querySelector('pre').innerText

    if (container.classList.contains("highlight-console")) {
        text = nxt_copy_console(text)
    }

    navigator.clipboard.writeText(text)

    console.log(text.length + " chars copied to clipboard")
}


function nxt_copy_console(text) {
    const result = []

    let heredoc = false
    let multi = false

    for (let line of text.split('\n')) {
        const trimmed = line.trim()

        if (!multi) {
            if (heredoc) {
                if (trimmed === heredoc) {
                    heredoc = false
                    line = trimmed
                }

                result.push(line)
                continue
            }

            switch (trimmed[0]) {
            case '$':
                line = trimmed.replace(/^\$\s*/, '')
                break
            case '#':
                line = trimmed.replace(/^#\s*/, 'sudo ')
                              .replace(/\|\s*/g, '| sudo ')
                break
            default:
                continue
            }

            line = line.replace(/\s+#.+$/, '')
        }

        const matches = trimmed.match(/<<\s*(\w+)/)
        if (matches) {
            heredoc = matches[1]
        }

        result.push(line)

        multi = (trimmed.substr(-1) === '\\')
    }

    return result.join('\n')
}


window.addEventListener("load", nxt_page_load)
