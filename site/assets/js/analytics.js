/* Google Analytics (GA4). Every page loads this file.
   Paste the Measurement ID from Google Analytics between the quotes,
   e.g. 'G-ABC123XYZ'. While it is empty, nothing is loaded or tracked. */
var GA_MEASUREMENT_ID = '';

(function () {
  if (!GA_MEASUREMENT_ID) return;
  var s = document.createElement('script');
  s.async = true;
  s.src = 'https://www.googletagmanager.com/gtag/js?id=' + GA_MEASUREMENT_ID;
  document.head.appendChild(s);
  window.dataLayer = window.dataLayer || [];
  window.gtag = function () { window.dataLayer.push(arguments); };
  window.gtag('js', new Date());
  window.gtag('config', GA_MEASUREMENT_ID);
})();
