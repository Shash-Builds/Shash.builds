/**
 * Level-Up Dashboard: the Sheet's private API.
 *
 * Paste into the Sheet: Extensions > Apps Script. Set a Script Property named
 * PASSPHRASE (Project Settings > Script Properties). Deploy > New deployment > Web app,
 * Execute as: Me, Who has access: Anyone. Every request must carry the passphrase,
 * for reads and writes, so the web app URL alone shows nothing.
 *
 * Requests: POST with a text/plain body of JSON (avoids a CORS preflight):
 *   {"pass": "...", "action": "read"}
 *   {"pass": "...", "action": "save", "tab": "days", "row": {...}}   days: same date updates the row
 *   {"pass": "...", "action": "setConfig", "key": "goal_usd", "value": "10000"}
 * MIT License, shash.builds.
 */
var TABS = ['days', 'sales', 'content', 'followers', 'reviews', 'config'];
var WRITABLE = ['days', 'sales', 'content', 'followers', 'reviews'];

function doPost(e) {
  var req;
  try { req = JSON.parse(e.postData.contents); } catch (err) { return out({ ok: false, error: 'Bad request' }); }
  var pass = PropertiesService.getScriptProperties().getProperty('PASSPHRASE');
  if (!pass) return out({ ok: false, error: 'Set the PASSPHRASE script property first.' });
  if (!same(String(req.pass || ''), pass)) { Utilities.sleep(800); return out({ ok: false, error: 'Wrong passphrase' }); }
  var lock = LockService.getScriptLock();
  lock.waitLock(10000);
  try {
    if (req.action === 'read') return out({ ok: true, data: readAll() });
    if (req.action === 'save') return out(save(req.tab, req.row || {}));
    if (req.action === 'setConfig') return out(setConfig(String(req.key || ''), req.value));
    return out({ ok: false, error: 'Unknown action' });
  } finally { lock.releaseLock(); }
}

function doGet() { return out({ ok: false, error: 'Use POST with the passphrase.' }); }

function same(a, b) {  // compare without stopping at the first difference
  var diff = a.length ^ b.length;
  for (var i = 0; i < Math.max(a.length, b.length); i++) diff |= (a.charCodeAt(i) || 0) ^ (b.charCodeAt(i) || 0);
  return diff === 0;
}

function out(obj) { return ContentService.createTextOutput(JSON.stringify(obj)).setMimeType(ContentService.MimeType.JSON); }

function sheet(name) {
  var s = SpreadsheetApp.getActiveSpreadsheet().getSheetByName(name);
  if (!s) throw new Error('Missing tab: ' + name);
  return s;
}

function headers(s) {
  var row = s.getRange(1, 1, 1, Math.max(1, s.getLastColumn())).getValues()[0];
  var h = [];
  for (var i = 0; i < row.length && String(row[i]).trim() !== ''; i++) h.push(String(row[i]).trim());
  return h;
}

function cell(v) {
  if (v instanceof Date) return Utilities.formatDate(v, Session.getScriptTimeZone(), 'yyyy-MM-dd');
  return v;
}

function readAll() {
  var data = {};
  TABS.forEach(function (name) {
    var s = SpreadsheetApp.getActiveSpreadsheet().getSheetByName(name);
    if (!s) { data[name] = []; return; }
    var h = headers(s);
    var n = s.getLastRow() - 1;
    if (n < 1 || !h.length) { data[name] = []; return; }
    data[name] = s.getRange(2, 1, n, h.length).getValues()
      .filter(function (r) { return r.some(function (v) { return v !== ''; }); })
      .map(function (r) { var o = {}; h.forEach(function (k, i) { o[k] = cell(r[i]); }); return o; });
  });
  return data;
}

function save(tab, row) {
  if (WRITABLE.indexOf(tab) < 0) return { ok: false, error: 'Tab not writable: ' + tab };
  var s = sheet(tab), h = headers(s);
  var values = h.map(function (k) { return row[k] === undefined || row[k] === null ? '' : row[k]; });
  if (tab === 'days' && row.date) {
    var n = s.getLastRow() - 1;
    if (n > 0) {
      var dates = s.getRange(2, 1, n, 1).getValues();
      for (var i = 0; i < dates.length; i++) {
        if (cell(dates[i][0]) === row.date) { s.getRange(i + 2, 1, 1, h.length).setValues([values]); return { ok: true, updated: true }; }
      }
    }
  }
  s.appendRow(values);
  return { ok: true, updated: false };
}

function setConfig(key, value) {
  if (!/^[a-z0-9_]{1,40}$/.test(key)) return { ok: false, error: 'Bad key' };
  var s = sheet('config'), n = s.getLastRow() - 1;
  if (n > 0) {
    var keys = s.getRange(2, 1, n, 1).getValues();
    for (var i = 0; i < keys.length; i++) if (String(keys[i][0]) === key) { s.getRange(i + 2, 2).setValue(value); return { ok: true }; }
  }
  s.appendRow([key, value, '']);
  return { ok: true };
}
