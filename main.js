const { exec } = require('child_process')

const Koa = require('koa')
const app = new Koa()


const fs = require('fs')


const create_list = filenames => {
  return `${filenames.map(name => `<a href='sort/${name}'>${name}</a>`).join('<br />')}`
}

const list_files = async () => {
  return new Promise(resolve => {
    fs.readdir('./documents/', (err, files) => {
      if (err) {
        resolve([])
      }
      resolve(files)
    })
  })
}

const last = arr => arr[arr.length - 1]

const print_record = record => {
  let [ path, relevance ] = record.slice(1, -1).split(',')
  path = path.slice(3, -1)

  return `<a href='/${path}'>${last(path.split('/'))}</a> relevance: ${relevance}`
}

const find_relevance = async docname => {
  return new Promise(resolve => {
    const script = exec(`./find_similar.py ${docname}`, (err, stdout, stderr) => {
      resolve(stdout.split('\n').map(print_record).join('<br />'))
    })
  })
}

const show_content = async docname => {
  return new Promise(resolve => {
    fs.readFile(`./documents/${docname}`, (err, data) => {
      resolve(data.toString())
    });
  })
}

app.use(async ctx => {
  if (ctx.url === '/') {
    ctx.body = create_list(await list_files())
  } else if (ctx.url.match('sort/')) {
    const docname = last(ctx.url.split('/'))
    ctx.body = await find_relevance(docname)
  } else if (ctx.url.match('documents/')) {
    const docname = last(ctx.url.split('/'))
    ctx.body = await show_content(docname)
  }
});

app.listen(3000);