// A comment
// Data types in JS
// String,=> "",'', ``
// Number,=> 1, 2, 3
// Boolean,=> true, false
// Object, => {name: "John", age: 30} - python dicts
// Array, => [1, 2, 3]

// Null => A value that means nothing/empty
// Undefined => Defualt value when nothing is set

// DOM - Document Object Model
// https://www.w3schools.com/js/js_number_methods.asp


// How to get HTML elements from JS?

// method 1
const gridElement = document.getElementById("product-grid");

// method 2; not used, demonstration only
const gridElement2 = document.querySelector("#product-grid");

// String methods
// https://www.w3schools.com/js/js_strings.asp

const name = "User"

const welcomeMessage = `Hello, ${name} welcome to our mini shop!`;

const taglineElement=document.getElementById("tagline");

taglineElement.innerHTML = welcomeMessage;

function renderProduct(name, price, description, stock) {
    const divElement = document.createElement("div");
    divElement.className = "product-item"

    const h2Element = document.createElement("h2");
    h2Element.textContent = name;
    
    const priceElement = document.createElement("p"); 
    priceElement.className = "price";
    priceElement.textContent = `Price: GHS${price.toFixed(2)}`;

    const descriptionElement = document.createElement("p");
    descriptionElement.className = "description";
    descriptionElement.textContent = `Description: ${description}`;

    const stockElement = document.createElement("p");
    stockElement.className = "stock";
    stockElement.textContent = `Remaining: ${stock}`;

    divElement.appendChild(h2Element);
    divElement.appendChild(priceElement);
    divElement.appendChild(descriptionElement);
    divElement.appendChild(stockElement);

    gridElement.appendChild(divElement);

}
    

const  product = [
    {
        name: "Headphones",
        price: 2900.5,
        description: "Apple headphones",
        stock: 10
    },
    {
        name: "Laptop",
        price: 34000,
        description: "M6 series macbook pro",
        stock: 10
    },
    {
        name: "Tablet",
        price: 1850,
        description: "This is a nice tablet",
        stock: 10
    },
    {
        name: "Smartwatch",
        price: 999.50,
        description: "This is the real Smartwatch pro",
        stock: 50
    },
    {
        name: "Airpods",
        price: 800,
        description: "This is the original airpod pro for iphones 18 and above",
        stock: 200
    }
]


product.forEach((item) => {
    renderProduct(item.name, item.price, item.description, item.stock);
});


