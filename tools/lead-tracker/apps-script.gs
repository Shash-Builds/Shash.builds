/**
 * Lead tracker: receives website form posts and adds a row to the "Leads" tab.
 * Setup: in the Google Sheet, Extensions > Apps Script, paste this, Save,
 * then Deploy > New deployment > Web app > Execute as: Me, Who has access: Anyone.
 * Copy the web app URL into capture.js (SHEET_URL).
 */
function doPost(e) {
  var p = e.parameter;
  var sheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName('Leads');
  sheet.appendRow([
    Utilities.formatDate(new Date(), Session.getScriptTimeZone(), 'yyyy-MM-dd'),
    p.name || '', p.phone || '', p.email || '', p.job || '',
    p.source || 'Other', p.page || '', 'New', '', ''
  ]);
  return ContentService.createTextOutput(JSON.stringify({ ok: true }))
    .setMimeType(ContentService.MimeType.JSON);
}
