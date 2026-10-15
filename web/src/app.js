/* 表格查看器 - 前端逻辑
 * 功能：离线打开/编辑 xlsx（Luckysheet 全功能：编辑/筛选/排序/求和/插入删除行列/合并/选择反选），
 *       导出 xlsx（SheetJS），深浅色自适应，iOS 桥（appfile:// 协议 + messageHandler）。
 */
(function () {
  'use strict';

  var isNative = !!(window.webkit && window.webkit.messageHandlers && window.webkit.messageHandlers.xlsxBridge);
  var currentFileName = null;
  var sheetData = null;          // luckysheet.create 时传入的 data
  var loading = false;

  var $empty = document.getElementById('empty');
  var $emptyTip = $empty.querySelector('.tip');
  var $luckysheet = document.getElementById('luckysheet');
  var $fileInput = document.getElementById('fileInput');

  /* ===== 深浅色（跟随系统，铁律） ===== */
  function luckysheetTheme(dark) {
    // Luckysheet 无内置暗色主题：canvas 靠 CSS 反转，DOM 容器这里直接注入内联背景
    var root = document.getElementById('luckysheet');
    if (!root) return;
    var els = root.querySelectorAll('[class*="toolbar"], [class*="sheets"], [class*="count"], [class*="formula"], [class*="scrollbar"], #luckysheet-sheet-area');
    for (var i = 0; i < els.length; i++) {
      els[i].style.background = dark ? '#000000' : '';
      els[i].style.color = dark ? '#ffffff' : '';
    }
  }
  function applyTheme(dark) {
    document.body.classList.toggle('dark', dark);
    luckysheetTheme(dark);
  }
  var mq = window.matchMedia('(prefers-color-scheme: dark)');
  applyTheme(mq.matches);
  if (mq.addEventListener) {
    mq.addEventListener('change', function (e) { applyTheme(e.matches); });
  } else if (mq.addListener) {
    mq.addListener(function (e) { applyTheme(e.matches); });
  }

  /* ===== 原生桥 ===== */
  function callNative(msg) {
    if (isNative) {
      window.webkit.messageHandlers.xlsxBridge.postMessage(msg);
    }
  }

  /* iOS 原生回调（Swift evaluateJavaScript 调用） */
  window.__onFileLoaded = function (name) { loadFileByName(name); };
  window.__onFileSaved = function (ok) {
    alert(ok ? '已保存到“表格查看器”文件夹' : '保存失败');
  };

  /* ===== 打开 ===== */
  function openFile() {
    if (loading) return;
    if (isNative) {
      callNative({ action: 'open' });
    } else {
      $fileInput.click();
    }
  }

  $fileInput.addEventListener('change', function () {
    var f = $fileInput.files && $fileInput.files[0];
    if (!f) return;
    $fileInput.value = '';
    loadFileFromBlob(f, f.name);
  });

  /* ===== 加载文件 ===== */
  function showLoading(name) {
    $empty.style.display = 'flex';
    $emptyTip.textContent = '正在打开 ' + name + ' …';
    document.getElementById('btnEmptyOpen').style.display = 'none';
  }
  function hideEmpty() {
    $empty.style.display = 'none';
  }

  function loadFileByName(name) {
    if (loading) return;
    loading = true;
    showLoading(name);
    fetch('appfile://files/' + encodeURIComponent(name))
      .then(function (r) {
        if (!r.ok) throw new Error('文件读取失败');
        return r.arrayBuffer();
      })
      .then(function (buf) {
        var file = new File([buf], name, { type: 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet' });
        loadFileFromBlob(file, name);
      })
      .catch(function (err) {
        alert('打开失败：' + err.message);
        resetEmpty();
        loading = false;
      });
  }

  function loadFileFromBlob(blob, name) {
    if (!window.LuckyExcel) {
      alert('表格引擎加载失败');
      resetEmpty();
      loading = false;
      return;
    }
    LuckyExcel.transformExcelToLucky(blob, function (exportJson, luckysheetfile) {
      if (!exportJson || !exportJson.sheets || exportJson.sheets.length === 0) {
        alert('无法解析该文件（仅支持 xlsx / xls）');
        resetEmpty();
        loading = false;
        return;
      }
      openInLuckysheet(exportJson.sheets, name);
    }, function (err) {
      alert('解析失败：' + (err && err.message ? err.message : err));
      resetEmpty();
      loading = false;
    });
  }

  function resetEmpty() {
    $emptyTip.textContent = '尚未打开文件';
    document.getElementById('btnEmptyOpen').style.display = 'block';
  }

  function openInLuckysheet(sheets, name) {
    currentFileName = name;
    sheetData = sheets;
    try {
      luckysheet.create({
        container: 'luckysheet',
        lang: 'zh',
        title: name,
        data: sheets,
        allowUpdate: false
      });
      hideEmpty();
      document.getElementById('btnSave').disabled = false;
      // create 后按当前主题注入深色（创建出来的 DOM 需要再覆盖一次）
      luckysheetTheme(mq.matches);
    } catch (e) {
      alert('表格初始化失败：' + e.message);
      resetEmpty();
    }
    loading = false;
  }

  /* ===== 保存 / 导出 xlsx（SheetJS） ===== */
  function cellToValue(cell) {
    if (!cell) return '';
    if (cell.v !== undefined && cell.v !== null && typeof cell.v !== 'object') return cell.v;
    return (cell.m !== undefined && cell.m !== null) ? cell.m : '';
  }
  function luckysheetToWorkbook(fileData) {
    var wb = XLSX.utils.book_new();
    (fileData || []).forEach(function (sheet) {
      var rows = (sheet && sheet.data) ? sheet.data : [];   // 行数组：rows[r] = 该行 cells 数组
      var aoa = [];
      for (var r = 0; r < rows.length; r++) {
        var row = rows[r] || [];
        aoa[r] = [];
        for (var c = 0; c < row.length; c++) aoa[r][c] = cellToValue(row[c]);
      }
      var ws = XLSX.utils.aoa_to_sheet(aoa);
      XLSX.utils.book_append_sheet(wb, ws, (sheet.name || 'Sheet1').slice(0, 31));
    });
    return wb;
  }

  function saveFile() {
    if (!currentFileName) return;
    var fileData = null;
    try {
      fileData = luckysheet.getluckysheetfile();
    } catch (e) {
      alert('读取表格数据失败：' + e.message);
      return;
    }
    var wb;
    try {
      wb = luckysheetToWorkbook(fileData);
      var out = XLSX.write(wb, { type: 'array', bookType: 'xlsx' });
      var base = arrayBufferToBase64(out);
      var saveName = currentFileName.replace(/\.(xlsx|xls|csv)$/i, '') + '_已编辑.xlsx';
      if (isNative) {
        callNative({ action: 'save', name: saveName, data: base });
      } else {
        downloadBase64(base, saveName);
      }
    } catch (e) {
      alert('导出失败：' + e.message);
    }
  }

  function arrayBufferToBase64(buffer) {
    var bytes = new Uint8Array(buffer);
    var chunks = [];
    var CHUNK = 0x8000;
    for (var i = 0; i < bytes.length; i += CHUNK) {
      chunks.push(String.fromCharCode.apply(null, bytes.subarray(i, i + CHUNK)));
    }
    return btoa(chunks.join(''));
  }

  function downloadBase64(base, name) {
    var a = document.createElement('a');
    a.href = 'data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,' + base;
    a.download = name;
    document.body.appendChild(a);
    a.click();
    setTimeout(function () { document.body.removeChild(a); }, 100);
  }

  /* ===== 事件绑定 ===== */
  document.getElementById('btnOpen').addEventListener('click', openFile);
  document.getElementById('btnEmptyOpen').addEventListener('click', openFile);
  document.getElementById('btnSave').addEventListener('click', saveFile);
  document.getElementById('btnSave').disabled = true;

  /* ===== 启动：自动打开原生传入的文件 ===== */
  var params = new URLSearchParams(window.location.search);
  var initialFile = params.get('file');
  if (initialFile) {
    loadFileByName(initialFile);
  }

  window.__xlsxViewerReady = true;
})();
