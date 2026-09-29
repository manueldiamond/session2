// Mini Shop - cleaned frontend script
// This file talks to the FastAPI back-end and draws products on the page.

// Grab the grid where all product cards will live.
const productGrid = document.getElementById("product-grid");

// Greet the shopper at the top of the page.
const userName = "User";

const BASE_API_URL = "http://localhost:8910";

function updateWelcomeMessage(userName) {
	let welcomeMessage;
	if (userName) {
		welcomeMessage = `Hello, ${userName} welcome to our mini shop!`;
	} else {
		welcomeMessage = `Welcome to our mini shop!`;
	}
	const taglineElement = document.getElementById("tagline");
	taglineElement.textContent = welcomeMessage;
}

// Build one product card and add it to the grid.
function renderProduct(name, price, description, stock, id) {
	// Outer card.
	const card = document.createElement("div");
	card.className = "product-item";

	// Product image (same placeholder for every item).
	const productImage = document.createElement("img");
	productImage.className = "product-image";
	productImage.src = "0204.jpg";

	// Product name.
	const title = document.createElement("h2");
	title.textContent = name;

	// Row that holds price on the left and stock on the right.
	const titleRow = document.createElement("div");
	titleRow.className = "product-title";

	const priceElement = document.createElement("p");
	priceElement.className = "price";
	priceElement.textContent = `Price: GHS${price.toFixed(2)}`;

	const stockElement = document.createElement("p");
	stockElement.className = "stock";
	stockElement.textContent = `Remaining: ${stock}`;

	titleRow.appendChild(priceElement);
	titleRow.appendChild(stockElement);

	// Long text about the product.
	const descriptionElement = document.createElement("p");
	descriptionElement.className = "description";
	descriptionElement.textContent = `Description: ${description}`;

	// Two buttons under each product.
	const buttons = document.createElement("div");
	buttons.className = "buttons-container";

	const addToCartButton = document.createElement("button");
	addToCartButton.textContent = "Add to Cart";
	addToCartButton.onclick = () => addToCart(id);

	const buyNowButton = document.createElement("button");
	buyNowButton.className = "primary";
	buyNowButton.textContent = "Buy Now";

	buttons.appendChild(addToCartButton);
	buttons.appendChild(buyNowButton);

	// Put the card together in order, then show it.
	card.appendChild(productImage);
	card.appendChild(titleRow);
	card.appendChild(title);
	card.appendChild(descriptionElement);
	card.appendChild(buttons);
	productGrid.appendChild(card);
}

// Load all products from the back-end.
// Uses promise chains (.then) because it is a straight line:
// fetch -> parse JSON -> draw each item.
function queryProducts() {
	fetch("http://localhost:8003/products")
		.then((response) => response.json())
		.then((products) => {
			products.forEach((item) => {
				renderProduct(
					item.name,
					item.price,
					item.description,
					item.stock,
					item.id,
				);
			});
		})
		.catch(() => {
			console.log("Something went wrong");
		});
}

// Add one product to the cart.
// Uses async/await because we need to branch:
// first wait for the reply, then decide good vs bad.
// Key detail: fetch does NOT throw on 400/404.
// A 400/404 is still a full reply, so we must check response.ok by hand.
// Good reply looks like { message, products }.
// Bad reply looks like { detail }.
async function addToCart(id) {
	try {
		const response = await fetch(
			"http://localhost:8003/products/add-to-cart/" + id,
			{
				method: "PUT",
			},
		);
		const data = await response.json();

		// Server said no: show the true error word from `detail`.
		if (!response.ok) {
			alert(data.detail || " An unexpected error occured");
			return;
		}

		// Server said yes: show the success word from `message`.
		alert(`${data.message} \n ${data.products}`);
	} catch (e) {
		// Only runs on net cuts or bad JSON, not on 400/404.
		alert(e.detail || " An unexpected error occured");
	}
}

/*
queryProducts();
*/



const loginForm = document.getElementById("login-form");


let accessToken;



function connectLogin(){
	loginForm.addEventListener("submit", (e) => {
		e.preventDefault();

        const usernameElement = document.getElementById("username");
		const passwordElement = document.getElementById("password");

		const username = usernameElement.value;
		const password = passwordElement.value;

		login(username, password).then(checkLogin);
	});
}

async function login(username, password) {
	try {
		const response = await fetch(`${BASE_API_URL}/login`, {
			method: "POST",
			headers: {
				"Content-Type": "application/json",
			},
			body: JSON.stringify({
				username,
				password,
			}),
		});

		const data = await response.json();

		if (!response.ok) {
			throw new Error(data.detail);
		}

		accessToken = data.access_token;	

	}catch (e) {
		alert("Failed to login")
	}
}


async function getUserProfile() {
	try {
		const response = await fetch(`${BASE_API_URL}/user/me`, {
			method: "GET",
			headers: {
				"Content-Type": "application/json",
				"Authorization": `Bearer ${accessToken}`,
			},
		});

		if (!response.ok) {
			throw new Error(data.detail);
		}

		const data = await response.json();

		updateWelcomeMessage(data.user.username);
	} catch (e) {
		alert("Failed to get user profile")
	}
}

function checkLogin(){
	const isloggedIn = !!accessToken

	if(isloggedIn){
		loginForm.style.visibility="hidden"
	}else {
		loginForm.style.visibility="visible"
	}

	getUserProfile()
}

connectLogin();