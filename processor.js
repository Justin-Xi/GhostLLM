fs = require('node:fs')

table = require('./table_data.json')

discard_reg = /【|】|P2|废弃|\(|（/

function modifyObject(obj) {
  if (obj !== null && typeof obj === 'object') {
    Object.keys(obj).forEach(key => {
      if (discard_reg.test(key) || key === '') {
        delete obj[key]
      }

      if (obj[key] !== null && typeof obj[key] === 'object') {
        if (discard_reg.test(key) || key === '') {
          delete obj[key]
        }
        obj[key.trim()] = { name: '', ...modifyObject(obj[key]) }
      } else {
        delete obj[key]
      }
    })
  }
  return obj
}

// Object.keys(table).filter(key => /P2|废弃|【|】/.test(key)).concat(['名词解释', "色彩标记说明", "定时触发", "时间字段", '']).forEach(key => delete table[key])
['名词解释', "色彩标记说明", "定时触发", "时间字段", ''].forEach(key => delete table[key])

fs.writeFileSync('name_mapping.json', JSON.stringify(modifyObject(table), null, 2))
