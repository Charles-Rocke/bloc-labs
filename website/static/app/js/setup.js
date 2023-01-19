'use strict';

/* change left side color
document.querySelector(".col1").style.backgroundColor = "#00FF00";

// get status of switch
const switchBtn = document.getElementById("flexSwitchCheckDefault");
// get index view
const indexView = document.querySelector(".index");

const templateView = document.querySelector(".temp");



switchBtn.addEventListener("click", function() {
	// display current status of switch button
	console.log(switchBtn.checked);
	// console.log(switchBtn.checked);
	if (switchBtn.checked) {
		document.querySelector(".col1").style.backgroundColor = "#DE73FF";
		document.querySelector(".col2").style.backgroundColor = "#00FF00";
		
	}
	else {
		document.querySelector(".col1").style.backgroundColor = "#00FF00";
		document.querySelector(".col2").style.backgroundColor = "#DE73FF";
	}
})
*/

// 1. Allow user to set a field (bootstrap)


// 2. Allow user to set brand colors (bootstrap)
// const primaryColor = document.getElementById("primary-color").value;
// const secondaryColor = document.getElementById("secondary-color").value;


// 3. Allow user to set logo (bootstrap)
let logo;
const header = document.querySelector(".setup-signup-header");
const fieldName = document.querySelector(".field-name-value");
const headerMessage = document.querySelector(".setup-signup-header-message");
const companyName = document.querySelector(".company-name");
const primaryColor = document.querySelector(".primary-color");
const secondaryColor = document.querySelector(".secondary-color");


// 3. Set logo
const imageInput = document.querySelector("#file");
logo = "";
imageInput.addEventListener("change", function() {
	const reader = new FileReader();
	reader.addEventListener("load", () => {
		logo = reader.result;
		companyName.classList.add("hidden");
		document.querySelector("#display_image").style.backgroundImage = `url(${logo})`;
	});
	reader.readAsDataURL(this.files[0]);

});

// 4. Change content when submitted
document.querySelector(".set-container").addEventListener("change", function(e) {
	// 1. Set field
	document.querySelector(".field-name").textContent = fieldName.value;
	document.querySelector(".input100").placeholder = `Enter ${fieldName.value}`;
	// edit header message after setting field name
	headerMessage.textContent = `Enter your ${fieldName.value.toLowerCase()} below to sign up for an example account`;

	// 2. Set brand colors
	document.querySelector(".login100-form-bgbtn").style.background = `-webkit-linear-gradient(right, ${primaryColor.value}, ${secondaryColor.value}, ${primaryColor.value}, ${secondaryColor.value})`;
	document.querySelector(".login100-form-bgbtn").style.background = `-o-linear-gradient(right, ${primaryColor.value}, ${secondaryColor.value}, ${primaryColor.value}, ${secondaryColor.value})`;
	document.querySelector(".login100-form-bgbtn").style.background = `-moz-linear-gradient(right, ${primaryColor.value}, ${secondaryColor.value}, ${primaryColor.value}, ${secondaryColor.value})`;
	document.querySelector(".login100-form-bgbtn").style.background = `linear-gradient(right, ${primaryColor.value}, ${secondaryColor.value}, ${primaryColor.value}, ${secondaryColor.value})`;

	// set header if logo isn't filled
	if ((imageInput.value.length === 0) && (header.value)){
		document.querySelector("#display_image").textContent = header.value;
		//document.querySelector("#displayImage").textContent = companyName;
	}
	else{
		// remove company brand name
		const displayImage = document.querySelector("#display_image");
		displayImage.textContent = "";
	}
	
	
});



// set 'Your Brand' to company name

// changing the color of the button gradient
/*
background: `-webkit-linear-gradient(right, ${primaryColor}, ${secondaryColor}, ${primaryColor}, ${secondaryColor})`;

var dom = document.getElementById('mainHolder');
dom.style.backgroundImage = '-moz-linear-gradient('
        + orientation + ', ' + colorOne + ', ' + colorTwo + ')';
*/