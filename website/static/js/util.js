'use strict';

/*
Display current users form:
	When the page loads
	get user form data
	manipulate DOM with user form data
*/
window.addEventListener("load", async (event) => {
	console.log("loaded dashboard")
	
	const form = await fetch(
		"/form", {
			method: "POST",
			headers: {
				"Content-Type": "application/json",
			},
			body: JSON.stringify({
				"form": "request"
			}),
		}
	);

	const formJSON = await form.json();
	console.log("got form JSON")
	console.log("form json: ", formJSON);
	console.log(typeof formJSON);

	// manipulate DOM
	// 1. Set field
	document.querySelector(".field-name").textContent = formJSON.fieldName;
	document.querySelector(".input100").placeholder = `Enter ${formJSON.fieldName.toLowerCase()}`;
	// edit header message after setting field name
	headerMessage.textContent = `Enter your ${formJSON.fieldName.toLowerCase()} below to sign up for an example account`;

	// 2. Set brand colors
	document.querySelector(".login100-form-bgbtn").style.background = `-webkit-linear-gradient(right, ${formJSON.primaryColor}, ${formJSON.secondaryColor}, ${formJSON.primaryColor}, ${formJSON.secondaryColor})`;
	document.querySelector(".login100-form-bgbtn").style.background = `-o-linear-gradient(right, ${formJSON.primaryColor}, ${formJSON.secondaryColor}, ${formJSON.primaryColor}, ${formJSON.secondaryColor})`;
	document.querySelector(".login100-form-bgbtn").style.background = `-moz-linear-gradient(right, ${formJSON.primaryColor}, ${formJSON.secondaryColor}, ${formJSON.primaryColor}, ${formJSON.secondaryColor})`;
	document.querySelector(".login100-form-bgbtn").style.background = `linear-gradient(right, ${formJSON.primaryColor}, ${formJSON.secondaryColor}, ${formJSON.primaryColor}, ${formJSON.secondaryColor})`;

	// set header title (in place of logo)
	document.querySelector("#display_image").textContent = formJSON.header;
	// const { authenticated, message } = serverAuthJSON;
	// console.log({authenticated, message});
	// console.log(typeof {authenticated, message});
	// if (authenticated) {
	// 	window.location = "/account/setup";
	// } else {
	// 	console.log("not authenticated");
	// }
});