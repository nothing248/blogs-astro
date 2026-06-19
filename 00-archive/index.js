var Renderer = require('docsify-server-renderer')
var readFileSync = require('fs').readFileSync

// init
var renderer = new Renderer({
    template: readFileSync('./docs/index.template.html', 'utf-8'),
    config: {
        name: 'docsify',
        repo: 'docsifyjs/docsify'
    }
})

renderer.renderToString(url)
    .then(html => {
        console.log(html)
    })
    .catch(err => {})
