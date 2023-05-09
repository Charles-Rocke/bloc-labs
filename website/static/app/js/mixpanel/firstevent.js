// Track an event. It can be anything, but in this example, we're tracking a Signed Up event.
// Include a property about the signup, like the Signup Type
document
	// 1.EDIT your Signup button html 'id' below
  .getElementById("hello-btn")
  .addEventListener("click", async () => {
		alert("hello-btn was clicked");
		mixpanel.track("clicked hello button", {"clicked": "button"});
	});