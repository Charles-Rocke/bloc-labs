// Get the user's current time zone
const timezone = Intl.DateTimeFormat().resolvedOptions().timeZone;
  
// Set the value of the hidden input field
document.getElementById('timezone-input').value = timezone;