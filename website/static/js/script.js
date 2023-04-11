const { startRegistration, startAuthentication } = SimpleWebAuthnBrowser;

// Registration
const statusRegister = document.getElementById("statusRegister");
const dbgRegister = document.getElementById("dbgRegister");

// Authentication
const statusAuthenticate = document.getElementById("statusAuthenticate");
const dbgAuthenticate = document.getElementById("dbgAuthenticate");


/**
 * Helper methods
 */

function printToDebug(elemDebug, title, output) {
  if (elemDebug.innerHTML !== "") {
    elemDebug.innerHTML += "\n";
  }
  elemDebug.innerHTML += `// ${title}\n`;
  elemDebug.innerHTML += `${output}\n`;
}

function resetDebug(elemDebug) {
  elemDebug.innerHTML = "";
}

function printToStatus(elemStatus, output) {
  elemStatus.innerHTML = output;
}

function resetStatus(elemStatus) {
  elemStatus.innerHTML = "";
}

function getPassStatus() {
  return "✅";
}

function getFailureStatus(message) {
  return `🛑 (Reason: ${message})`;
}

/**
 * Register Button
 */
document
  .getElementById("btnRegister")
  .addEventListener("click", async () => {
    resetStatus(statusRegister);
    resetDebug(dbgRegister);

    // Get options
		console.log("getting options (sripts.js)")
    const resp = await fetch("/generate-registration-options");
	  console.log("RESP response: ",resp);
		console.log("RESP.challenge", resp.challenge)
    const opts = await resp.json();
		console.log("recieved registration response (scripts.js)");
    printToDebug(
      dbgRegister,
      "Registration Options",
      JSON.stringify(opts, null, 2)
    );

    // Start WebAuthn Registration
    let regResp;
    try {
	  	console.log("awaiting startRegistration (scripts.js)");
      regResp = await startRegistration(opts);
			console.log(regResp.challenge)
			// pop index 1 if it exists
			if (regResp){
				console.log("regResp exists");
			}
			if (regResp.transports) {
				console.log("regResp.transports exists");
				if (regResp.transports.length == 2) {
					console.log("regResp.transports.length is more than 1");
					regResp.transports.pop(1);
				}
			}
			
			console.log(regResp);
			console.log(typeof regResp);
	  	console.log("recieved startRegistration(opts) (scripts.js)");
      printToDebug(
        dbgRegister,
        "Registration Response",
        JSON.stringify(regResp, null, 2)
      );
    } catch (err) {
			if (err == undefined || typeof(err) == 'undefined') {
    		console.log("err is undefined");
			}
      printToStatus(statusRegister, getFailureStatus(err));
      throw new Error(err);
    }

    // Send response to server
    const verificationResp = await fetch(
      "/verify-registration-response",
      {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(regResp),
      }
    );

		console.log(verificationResp);
    // Report validation response
    const verificationRespJSON = await verificationResp.json();
		console.log(verificationRespJSON);
		console.log(typeof verificationRespJSON);
    const { verified, msg } = verificationRespJSON;
		console.log({verified, msg});
		document.querySelector(".biometric-msg").textContent = msg;
		console.log(typeof {verified, msg});
    if (verified) {
      printToStatus(statusRegister, getPassStatus());
			window.location = "/account/setup";
			alert(regResp.challenge);
    } else {
			console.log("not authenticated");
      printToStatus(statusRegister, getFailureStatus(err));
    }
    printToDebug(
      dbgRegister,
      "Verification Response",
      JSON.stringify(verificationRespJSON, null, 2)
    );
	// send data to python server
	// if verificationRespJSON property value == true => redirect to logged in screen
	// else registration verification not valid
	// const serverAuth = await fetch(
 //      "/registration",
 //      {
 //        method: "POST",
 //        headers: {
 //          "Content-Type": "application/json",
 //        },
 //        body: JSON.stringify(verificationRespJSON),
 //      }
 //    );

	// 	console.log(serverAuth);
 //    // Report validation response
 //    const serverAuthJSON = await serverAuth.json();
	// 	console.log(serverAuthJSON);
	// 	console.log(typeof serverAuthJSON);
 //    const { authenticated, message } = serverAuthJSON;
	// 	console.log({authenticated, message});
	// 	console.log(typeof {authenticated, message});
 //    if (authenticated) {
 //      window.location = "/account/setup";
 //    } else {
 //      console.log("not authenticated");
 //    }
	/*
	if (verified == true){
		window.location = "/account/setup";
	} else{
		console.log("Something went wrong");
	}
 */
 
});


/**
 * Authenticate Button
 */
document
  .getElementById("btnAuthenticate")
  .addEventListener("click", async () => {
    resetStatus(statusAuthenticate);
    resetDebug(dbgAuthenticate);

    // Get options
    const resp = await fetch("/generate-authentication-options");
    const opts = await resp.json();
    printToDebug(
      dbgAuthenticate,
      "Authentication Options",
      JSON.stringify(opts, null, 2)
    );

    // Start WebAuthn Authentication
    let authResp;
    try {
		// begin bug
		/* bug - incredibly long wait on random devices */
		console.log("Starting Authentication")
      authResp = await startAuthentication(opts);
	  console.log("finished Authentication")
		console.log(authResp.challenge);
			alert(authResp.challenge)
      printToDebug(
        dbgAuthenticate,
        "Authentication Response",
        JSON.stringify(authResp, null, 2)
      ); // end bug
    } catch (err) {
      printToStatus(statusAuthenticate, getFailureStatus(err));
      throw new Error(err);
    }

	  // debugging
		console.log("fetching verification response");
    // Send response to server
    const verificationResp = await fetch(
      "/verify-authentication-response",
      {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(authResp),
      }
    );
	  // debugging
		console.log("retrieved verification response")
	  // debugging
		console.log("checking verification response")
    // Report validation response
    const verificationRespJSON = await verificationResp.json();
    const { verified, msg } = verificationRespJSON;
		console.log(verified, msg)
    if (verified) {
      printToStatus(statusAuthenticate, getPassStatus());
			window.location = "/dashboard/home";
			console.log(authResp.challenge)
    } else {
      printToStatus(statusAuthenticate, getFailureStatus(err));
			console.log("not authenticated");
    }
    printToDebug(
      dbgAuthenticate,
      "Verification Response",
      JSON.stringify(verificationRespJSON, null, 2)
    );
	  // debugging
		console.log("checked verification response")
	  // debugging
		console.log("ajax POST request")
	// // send data to python server
	// const serverAuth = await fetch(
 //      "/auth",
 //      {
 //        method: "POST",
 //        headers: {
 //          "Content-Type": "application/json",
 //        },
 //        body: JSON.stringify(verificationRespJSON),
 //      }
 //    );

	// 	console.log(serverAuth);
 //    // Report validation response
 //    const serverAuthJSON = await serverAuth.json();
	// 	console.log(serverAuthJSON);
	// 	console.log(typeof serverAuthJSON);
 //    const { authenticated, message } = serverAuthJSON;
	// 	console.log({authenticated, message});
	// 	console.log(typeof {authenticated, message});
 //    if (authenticated) {
 //      window.location = "/dashboard/home";
 //    } else {
 //      console.log("not authenticated");
 //    }
});
