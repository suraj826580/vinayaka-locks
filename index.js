/* PRODUCTS */

const products = [

  {
    name:"Lock Body",
    category:"Lock Body",
    image:"lock-body.jpg",
    description:"Professional quality lock body suitable for door hardware applications."
  },

  {
    name:"Pull Handle",
    category:"Pull Handle",
    image:"pull-handle.jpg",
    description:"Durable pull handle designed for professional door applications."
  },

  {
    name:"Door Hardware",
    category:"Door Hardware",
    image:"door-hardware.jpg",
    description:"Professional door hardware solution for residential and commercial projects."
  },

  {
    name:"Architectural Hardware",
    category:"Door Hardware",
    image:"architectural-hardware.jpg",
    description:"Modern architectural hardware for professional projects."
  }

];


/* RENDER PRODUCTS */

const productsContainer =
  document.getElementById("products");

function renderProducts(){

  const search =
    document.getElementById("searchInput")
    .value
    .toLowerCase();

  const category =
    document.getElementById("categoryFilter")
    .value;

  const filtered =
    products.filter(product => {

      const matchesSearch =
        product.name
        .toLowerCase()
        .includes(search);

      const matchesCategory =
        category === "all" ||
        product.category === category;

      return matchesSearch && matchesCategory;

    });

  productsContainer.innerHTML = "";

  if(filtered.length === 0){

    productsContainer.innerHTML = `
      <p style="
        grid-column:1/-1;
        text-align:center;
        color:#9ca3af;
        padding:40px;
      ">
        No products found.
      </p>
    `;

    return;
  }

  filtered.forEach((product,index) => {

    const card = document.createElement("div");

    card.className = "product";

    card.innerHTML = `

      <div class="product-image">

        <img
          src="${product.image}"
          alt="${product.name}"
          loading="lazy"
        >

      </div>

      <div class="product-info">

        <h3>
          ${product.name}
        </h3>

        <p>
          ${product.category}
        </p>

        <button
          class="product-btn"
          onclick="openProduct(${index})"
        >
          View Product
        </button>

      </div>

    `;

    productsContainer.appendChild(card);

  });

}


/* SEARCH */

document
  .getElementById("searchInput")
  .addEventListener("input",renderProducts);


/* FILTER */

document
  .getElementById("categoryFilter")
  .addEventListener("change",renderProducts);


/* PRODUCT MODAL */

const modal =
  document.getElementById("productModal");

const modalTitle =
  document.getElementById("modalTitle");

const modalImage =
  document.getElementById("modalImage");

const modalDescription =
  document.getElementById("modalDescription");

const modalWhatsApp =
  document.getElementById("modalWhatsApp");


function openProduct(index){

  const product = products[index];

  modalTitle.textContent =
    product.name;

  modalImage.src =
    product.image;

  modalImage.alt =
    product.name;

  modalDescription.textContent =
    product.description;

  modalWhatsApp.href =
    "https://wa.me/919219609700?text=" +
    encodeURIComponent(
      "Hello Vinayak Locks, I am interested in " +
      product.name
    );

  modal.classList.add("active");

  document.body.style.overflow =
    "hidden";
}


function closeModal(){

  modal.classList.remove("active");

  document.body.style.overflow =
    "";
}

window.openProduct = openProduct;
window.closeModal = closeModal;


document
  .getElementById("modalClose")
  .addEventListener("click",closeModal);


modal.addEventListener("click",function(e){

  if(e.target === modal){
    closeModal();
  }

});


/* MOBILE MENU */

const menuToggle =
  document.getElementById("menuToggle");

const mainNav =
  document.getElementById("mainNav");


menuToggle.addEventListener("click",function(){

  const opened =
    mainNav.classList.toggle("active");

  menuToggle.setAttribute(
    "aria-expanded",
    opened
  );

});


/* CLOSE MOBILE MENU AFTER CLICK */

mainNav
  .querySelectorAll("a")
  .forEach(link => {

    link.addEventListener("click",function(){

      mainNav.classList.remove("active");

      menuToggle.setAttribute(
        "aria-expanded",
        "false"
      );

    });

  });


/* CLOSE MENU ON RESIZE */

window.addEventListener("resize",function(){

  if(window.innerWidth > 820){

    mainNav.classList.remove("active");

    menuToggle.setAttribute(
      "aria-expanded",
      "false"
    );

  }

});


/* WHATSAPP QUOTE FORM */

document
  .getElementById("quoteForm")
  .addEventListener("submit",function(e){

    e.preventDefault();

    const name =
      document.getElementById("name").value;

    const phone =
      document.getElementById("phone").value;

    const product =
      document.getElementById("product").value;

    const message =
      document.getElementById("message").value;

    const text =
      `Hello Vinayak Locks,

Name: ${name}
Phone: ${phone}
Product: ${product}
Requirement: ${message}`;

    const url =
      "https://wa.me/919219609700?text=" +
      encodeURIComponent(text);

    window.open(url,"_blank");

  });


/* INITIAL LOAD */

renderProducts();
