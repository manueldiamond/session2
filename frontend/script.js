const gridElement = document.getElementById("product-grid");

const gridElement2 = document.querySelector("#product-grid");

const name = "User";

const welcomeMessage = `Hello, ${name} welcome to our mini shop!`;

const taglineElement = document.getElementById("tagline");

taglineElement.textContent = welcomeMessage;

function renderProduct(name, price, description, stock, id) {
	const divElement = document.createElement("div");
	divElement.className = "product-item";

	const productImage = document.createElement("img");
	productImage.className = "product-image";
	productImage.src = "0204.jpg";

	const h2Element = document.createElement("h2");
	h2Element.textContent = name;

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

	const descriptionElement = document.createElement("p");
	descriptionElement.className = "description";
	descriptionElement.textContent = `Description: ${description}`;

	const buttons = document.createElement("div");
	buttons.className = "buttons-container";
	const addToCartButton = document.createElement("button");
	const button2 = document.createElement("button");
	button2.className = "primary";

	addToCartButton.textContent = "Add to Cart";
	button2.textContent = "Buy Now";

	addToCartButton.onclick = () => addToCart(id);

	buttons.appendChild(addToCartButton);
	buttons.appendChild(button2);

	divElement.appendChild(productImage);
	divElement.appendChild(titleRow);

	divElement.appendChild(h2Element);
	divElement.appendChild(descriptionElement);
	divElement.appendChild(buttons);

	gridElement.appendChild(divElement);
}

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

async function addToCart(id) {
	try {
		const response = await fetch(
			"http://localhost:8003/products/add-to-cart/" + id,
			{
				method: "PUT",
			},
		);
		const data = await response.json();
		if (!response.ok) {
			alert(data.detail || " An unexpected error occured");
			return;
		}
		alert(`${data.message} \n ${data.products}`);
	} catch (e) {
		alert(e.detail || " An unexpected error occured");
	}
}

queryProducts();
