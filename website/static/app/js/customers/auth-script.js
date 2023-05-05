// import blocJS auth methods
const { startSignup, startLogin } = blocJS;
/**
 * Signup Button
 */
document
	// 1. EDIT your Signup button html 'id' below
  .getElementById("yourSignupBtnIDHere")
  .addEventListener("click", async () => {
    /* Generate signup options for your user */
		// 2. EDIT this fetch request your route that will make the api request to our server
    const resp = await fetch("/your-signup-route-here");
    const opts = await resp.json();
    // Start WebAuthn Registration
    let regResp;
    try {
      regResp = await startSignup(opts);
			// if more than one transport pop one (only one is needed)
			if (regResp.transports) {
				if (regResp.transports.length == 2) {
					regResp.transports.pop(1);
				}
			}
    } catch (err) {
			if (err == undefined || typeof(err) == 'undefined') {
    		console.log("err is undefined");
			}
      throw new Error(err);
    }
    /* Send response to server */
		// 3. EDIT this fetch request your route that will make the api request to our server
    const verificationResp = await fetch(
      "/your-verify-signup-route-here",
      {
        method: "POST",
				mode: 'cors',
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(regResp),
      }
    );
    // Report validation response
    const verificationRespJSON = await verificationResp.json();
    const { verified, msg } = verificationRespJSON;
    if (verified) {
			/* Redirect to your "login required" page */
			// 4. EDIT this location to redirect the user to your login required page
			window.location = "/your/redirect/location/here";
    } else {
			console.log("not authenticated");
    }
});


/**
 * Login Button
 */
document
	// 5. EDIT your Login button html 'id' below
  .getElementById("yourLoginBtnIDHere")
  .addEventListener("click", async () => {
    /* Generate login options for your user */
		// 6. EDIT this fetch request your route that will make the api request to our server
    const resp = await fetch("/your-login-route-here");
    const opts = await resp.json();
    // Start bloc Login
    let authResp;
    try {
    authResp = await startLogin(opts);
    } catch (err) {
      throw new Error(err);
    }
    /* Send response to server */
		// 7. EDIT this fetch request your route that will make the api request to our server
    const verificationResp = await fetch(
      "/your-verify-login-route-here",
      {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(authResp),
      }
    );
    // Report validation response
    const verificationRespJSON = await verificationResp.json();
    const { verified, msg } = verificationRespJSON;
		if (verified) {
			/* Redirect to your "login required" page */
			// 8. EDIT this location to redirect the user to your login required page
			window.location = "/your/redirect/location/here";
    } else {
			console.log("not authenticated");
    }
});