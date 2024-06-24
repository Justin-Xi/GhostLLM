function convertDoc2Json() {
  var body = DocumentApp.getActiveDocument().getBody();
  // var elements = DocumentApp.getActiveDocument().getBody().getParagraphs();

  var result = {};
  var currentModule = '';
  var currentFunction = '';
  var parseMode = ''; // 用于指示当前解析的是in还是out
  var numChildren = body.getNumChildren();
  var out = 0
  for (var i = 0; i < numChildren; i++) {
    var element = body.getChild(i);

    var type = element.getType()
    var heading = type !=  DocumentApp.ElementType.TABLE ? element.asParagraph().getHeading() : 'table'
    var text = type !=  DocumentApp.ElementType.TABLE ? element.asParagraph().getText().trim() : ''
  // for (var i = 0; i < elements.length; i++) {
  //   var element = elements[i];
    var text = element.getText().trim();

    if (heading == DocumentApp.ParagraphHeading.HEADING2) {
      parseMode = 'mod_desc'
      currentModule = text;
      result[currentModule] = {};
    } else if (heading == DocumentApp.ParagraphHeading.HEADING3) {
      out = 0
      currentFunction = text;
      parseMode = ''; // 重置parseMode
      result[currentModule][currentFunction] = {}
    } else if (text === '函数描述') {
      if (currentFunction == '' || currentModule == '') continue;
      parseMode = 'func_desc'
    } else if (text === '入参字段') {
      if (currentFunction == '' || currentModule == '') continue;
      parseMode = 'in';
    } else if (text === '返回结果') {
      if (currentFunction == '' || currentModule == '') continue;
      if (/^out/.test(parseMode)) parseMode = 'out'+(++out);
      else parseMode = 'out';
    } else if (type == DocumentApp.ElementType.TABLE) {

      if (currentFunction == '' || currentModule == '') continue;

      var table = element.asTable();

      var rows = table.getNumRows();
      var headerRow = table.getRow(0)
      for (var r = 1; r < rows; r++) {
        var row = table.getRow(r);
        var fieldName = row.getCell(0).getText().trim()
        fieldObj = {}
        for (var c = 1; c < row.getNumCells(); c++) {
          fieldObj[headerRow.getCell(c).getText().trim()] = row.getCell(c).getText().trim()
        }

        result[currentModule][currentFunction][parseMode] = result[currentModule][currentFunction][parseMode] || {};
        result[currentModule][currentFunction][parseMode][fieldName] = fieldObj;
      }
    } else if (heading == DocumentApp.ParagraphHeading.NORMAL) {
        if (parseMode=='mod_desc' && currentModule!='') {
          if (text != '') result[currentModule]['description'] = text || '无'
        }
        if (parseMode=='func_desc' && currentModule!='' && currentFunction!='') {
          if (text != '') result[currentModule][currentFunction]['description'] = text || '无'
        }
    }
  }

  var json_text = JSON.stringify(result, null, 2)
  // Logger.log(json_text);


  var file = DriveApp.createFile('table_data.json', json_text);
  Logger.log('File URL: ' + file.getUrl());

  var recipient = 'tianyong@thinredline.com.cn'; // 替换为目标邮箱地址
  // var recipient = 'tianyong@thinredline.com.cn,zhaoguotao@thinredline.com.cn,sunhongjie@thinredline.com.cn,tianyuying@thinredline.com.cn,zhangyun@thinredline.com.cn,xiajinxi@thinredline.com.cn,sunmaosen@thinredline.com.cn'; // 替换为目标邮箱地址
  // var recipient = 'hsy377545335@gmail.com'; // 替换为目标邮箱地址
  var subject = 'Function in JSON - P1/P2...可以跳过';
  var body = 'Please find the attached JSON file containing the function definition. 函数名在json的第一级Key值，如果其中包括【】说明，则按照说明要求。P1/P2...可以跳过，暂时不做';
  MailApp.sendEmail({ to: recipient, subject: subject, body: body, attachments: [file] });
}
