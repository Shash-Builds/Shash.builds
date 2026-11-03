// Lead tracker: works out where a visitor came from and sends the form to the Google Sheet.
// Add to the site: <script src="capture.js" defer></script>, and give the quote form id="quote-form".
(function () {
  var SHEET_URL = 'PASTE_WEB_APP_URL_HERE';

  function source() {
    var q = new URLSearchParams(location.search);
    var utm = (q.get('utm_source') || '').toLowerCase();
    if (q.get('gclid') || utm === 'google_ads') return 'Google Ads';
    if (utm) return utm.charAt(0).toUpperCase() + utm.slice(1);
    var r = document.referrer.toLowerCase();
    if (!r) return 'Direct';
    if (r.indexOf('google.') > -1) return 'Google';
    if (r.indexOf('facebook.') > -1 || r.indexOf('fb.') > -1) return 'Facebook';
    if (r.indexOf('instagram.') > -1) return 'Instagram';
    if (r.indexOf('chatgpt.') > -1 || r.indexOf('openai.') > -1 || r.indexOf('perplexity.') > -1) return 'AI search';
    return 'Other';
  }

  // Remember the first source for this visitor, so a later visit doesn't overwrite it.
  var src;
  try { src = localStorage.getItem('lead_source'); if (!src) { src = source(); localStorage.setItem('lead_source', src); } }
  catch (e) { src = source(); }

  var form = document.getElementById('quote-form');
  if (!form) return;
  form.addEventListener('submit', function (ev) {
    ev.preventDefault();
    var data = new URLSearchParams(new FormData(form));
    data.set('source', src);
    data.set('page', location.pathname);
    fetch(SHEET_URL, { method: 'POST', body: data, mode: 'no-cors' })
      .then(function () { form.innerHTML = '<p>Thanks, we got it. We will call you soon.</p>'; })
      .catch(function () { form.innerHTML = '<p>Something went wrong. Please call us instead.</p>'; });
  });
})();
