// converting between base64 strings and array buffers
// https://stackoverflow.com/questions/21797299/convert-base64-string-to-arraybuffer
function _base64ToArrayBuffer(base64) {
    base64 = base64
        .replace(/-/g, '+')
        .replace(/_/g, '/')
        .replace(/\s/g, '')
    const binary_string = window.atob(base64);
    const len = binary_string.length;
    const bytes = new Uint8Array(len);
    for (let i = 0; i < len; i++) {
        bytes[i] = binary_string.charCodeAt(i);
    }
    return bytes.buffer;
}

// https://stackoverflow.com/questions/9267899/arraybuffer-to-base64-encoded-string
function _arrayBufferToBase64(buffer) {
    let binary = '';
    const bytes = new Uint8Array(buffer);
    const len = bytes.byteLength;
    for (let i = 0; i < len; i++) {
        binary += String.fromCharCode(bytes[i]);
    }
    return window.btoa(binary);
}

// Get options
console.log("getting options (sripts.js)")
const resp = await fetch("/generate-registration-options");
console.log("fetched registration options (scripts.js)");
console.log("awaiting registration response (scripts.js)");
const opts = await resp.json();
console.log("recieved registration response (scripts.js)");


// client creating user credentials
registrationOptions = // Copy and paste the options we printed in previous step:
                      // {"rp": {"name": "GitHub", "id": "github.com"}, ...}

const publicKeyCredentialCreationOptions = {
    ...registrationOptions,
    excludeCredentials: registrationOptions.excludeCredentials.map((credential) => {
        return {
            id: _base64ToArrayBuffer(credential.id),
            type: "public-key"
        }
    }),
    challenge: _base64ToArrayBuffer(registrationOptions.challenge),
    user: {
        ...registrationOptions.user,
        id: _base64ToArrayBuffer(registrationOptions.user.id),
    },
}

const credential = await navigator.credentials.create({
    publicKey: publicKeyCredentialCreationOptions
})

const registrationData = {
    type: credential.type,
    id: credential.id,
    authenticatorAttachment: credential.authenticatorAttachment,
    rawId: _arrayBufferToBase64(credential.rawId),
    response: {
        attestationObject: _arrayBufferToBase64(credential.response.attestationObject),
        clientDataJSON: _arrayBufferToBase64(credential.response.clientDataJSON)
    }
}

console.log(registrationData)

// client creating credential authentication
const authenticationOptions = // Copy and paste the authentication_options we printed in previous step

const publicKeyCredentialRequestOptions = {
    challenge: _base64ToArrayBuffer(authenticationOptions.challenge),
    allowCredentials: authenticationOptions.allowCredentials.map((credential) => {
        return {
            id: _base64ToArrayBuffer(credential.id),
            type: "public-key"
        }
    }),
    timeout: 60000,
}

const assertion = await navigator.credentials.get({
    publicKey: publicKeyCredentialRequestOptions
})

const authenticationData = {
    type: assertion.type,
    id: assertion.id,
    rawId: _arrayBufferToBase64(assertion.rawId),
    response: {
        authenticatorData: _arrayBufferToBase64(assertion.response.authenticatorData),
        clientDataJSON: _arrayBufferToBase64(assertion.response.clientDataJSON),
        signature: _arrayBufferToBase64(assertion.response.signature),
        userHandle: _arrayBufferToBase64(assertion.userHandle),
    }
}

console.log(authenticationData)
