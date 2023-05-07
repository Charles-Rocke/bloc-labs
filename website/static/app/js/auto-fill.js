// import blocJS auth methods
const { browserSupportsWebAuthnAutofill } = blocJS;

if (!browserSupportsWebAuthnAutofill()) {
	console.log('It seems this browser does not support WebAuthn...');
}

fetch('/generate-authentication-options')
.then((options) => {
	// Note the `true` argument here
	startAuthentication(options, true)
		.then(authResp => sendToServerForVerificationAndLogin)
		.catch(err => handleError);
});