import json

with open("products.json", "r", encoding="utf-8") as f:
    products_data = json.load(f)

products_json = json.dumps(products_data, indent=2, ensure_ascii=False)

js_template = """/* PRODUCTS DATASET (Extracted from catlague.pdf - 62 Products) */
const products = """ + products_json + """;

/* DOM ELEMENTS */
const productsContainer = document.getElementById("products");
const searchInput = document.getElementById("searchInput");
const clearSearchBtn = document.getElementById("clearSearchBtn");
const categoryFilter = document.getElementById("categoryFilter");
const productsCountText = document.getElementById("productsCountText");
const modal = document.getElementById("productModal");
const modalTitle = document.getElementById("modalTitle");
const modalImage = document.getElementById("modalImage");
const modalDescription = document.getElementById("modalDescription");
const modalWhatsApp = document.getElementById("modalWhatsApp");

let currentCategory = "all";

/* RENDER PRODUCTS */
function renderProducts() {
  if (!productsContainer) return;

  const search = searchInput ? searchInput.value.toLowerCase().trim() : "";
  const category = currentCategory;

  // Toggle clear search button
  if (clearSearchBtn) {
    if (search.length > 0) {
      clearSearchBtn.classList.add("active");
    } else {
      clearSearchBtn.classList.remove("active");
    }
  }

  const filtered = products.filter(product => {
    const matchesSearch =
      search === "" ||
      product.name.toLowerCase().includes(search) ||
      product.category.toLowerCase().includes(search) ||
      product.material.toLowerCase().includes(search) ||
      product.id.toLowerCase().includes(search) ||
      (product.models && product.models.some(m => m.toLowerCase().includes(search))) ||
      (product.modelSummary && product.modelSummary.toLowerCase().includes(search));

    const matchesCategory =
      category === "all" ||
      product.category === category;

    return matchesSearch && matchesCategory;
  });

  // Update count text
  if (productsCountText) {
    if (filtered.length === products.length) {
      productsCountText.textContent = `Showing all ${products.length} products`;
    } else {
      productsCountText.textContent = `Showing ${filtered.length} of ${products.length} products`;
    }
  }

  productsContainer.innerHTML = "";

  if (filtered.length === 0) {
    productsContainer.innerHTML = `
      <div class="no-products reveal active">
        <div class="no-products-icon">🔍</div>
        <h3>No Products Found</h3>
        <p>No products match your search criteria. Try a different term or category.</p>
        <button class="btn btn-primary" onclick="resetFilters()">Reset All Filters</button>
      </div>
    `;
    return;
  }

  filtered.forEach((product, idx) => {
    const actualIndex = products.findIndex(p => p.id === product.id);
    const card = document.createElement("div");
    card.className = "product-card reveal";
    card.style.setProperty("--delay", (idx % 6).toString());

    const modelBadges = (product.models && product.models.length > 0)
      ? product.models.slice(0, 3).map(m => `<span class="code-badge">${m}</span>`).join("") + (product.models.length > 3 ? `<span class="code-badge-more">+${product.models.length - 3}</span>` : "")
      : `<span class="code-badge">${product.id}</span>`;

    const waText = `Hello Vinayak Locks, I am inquiring about ${product.name} (${product.id} / ${product.modelSummary}). Please share catalog details and pricing.`;
    const waLink = "https://wa.me/919219609700?text=" + encodeURIComponent(waText);

    card.innerHTML = `
      <div class="product-card-image" onclick="openProduct(${actualIndex})">
        <img
          src="${product.image}"
          alt="${product.name}"
          loading="lazy"
          onerror="this.onerror=null; this.src='logo.PNG';"
        >
        <span class="product-category-tag">${product.category}</span>
      </div>

      <div class="product-card-body">
        <div class="product-header-info">
          <h3 class="product-title" onclick="openProduct(${actualIndex})">${product.name}</h3>
          <span class="product-id-tag">${product.id}</span>
        </div>

        <p class="product-material-spec">
          <strong>Spec:</strong> ${product.material}
        </p>

        <div class="product-models-list">
          ${modelBadges}
        </div>

        <div class="product-card-actions">
          <button
            class="btn-view-details"
            onclick="openProduct(${actualIndex})"
          >
            View Details
          </button>
          <a
            class="btn-card-whatsapp"
            href="${waLink}"
            target="_blank"
            title="Inquire on WhatsApp"
          >
            <span>Enquire Now</span> <span>💬</span>
          </a>
        </div>
      </div>
    `;

    productsContainer.appendChild(card);
  });

  // Trigger intersection observer on newly rendered cards
  initCardObserver();
}

/* CATEGORY FILTER HANDLING */
function selectChip(category) {
  currentCategory = category;

  // Update chips active state
  document.querySelectorAll(".chip-btn").forEach(chip => {
    if (chip.getAttribute("data-category") === category) {
      chip.classList.add("active");
    } else {
      chip.classList.remove("active");
    }
  });

  // Update dropdown
  if (categoryFilter) {
    categoryFilter.value = category;
  }

  renderProducts();
}

function filterByCategory(category) {
  selectChip(category);
  const catalogueSection = document.getElementById("catalogue");
  if (catalogueSection) {
    catalogueSection.scrollIntoView({ behavior: "smooth" });
  }
}

function clearSearch() {
  if (searchInput) {
    searchInput.value = "";
    searchInput.focus();
  }
  renderProducts();
}

function resetFilters() {
  if (searchInput) searchInput.value = "";
  selectChip("all");
}

/* PRODUCT MODAL */
function openProduct(index) {
  const product = products[index];
  if (!product) return;

  if (modalTitle) modalTitle.textContent = `${product.name} · ${product.category}`;
  if (modalImage) {
    modalImage.src = product.image;
    modalImage.alt = product.name;
  }

  if (modalDescription) {
    const featuresList = (product.features && product.features.length > 0)
      ? `<div class="modal-section">
          <h4>Key Features & Specifications:</h4>
          <ul class="modal-features-list">
            ${product.features.map(f => `<li>✓ ${f}</li>`).join("")}
          </ul>
        </div>`
      : "";

    const modelsList = (product.models && product.models.length > 0)
      ? `<div class="modal-section">
          <h4>Available Model Codes:</h4>
          <div class="modal-models-pills">
            ${product.models.map(m => `<span class="pill-badge">${m}</span>`).join("")}
          </div>
        </div>`
      : "";

    const finishesList = (product.finishes && product.finishes.length > 0)
      ? `<div class="modal-section">
          <h4>Available Finishes:</h4>
          <div class="modal-finishes-pills">
            ${product.finishes.map(fn => `<span class="finish-pill">🎨 ${fn}</span>`).join("")}
          </div>
        </div>`
      : "";

    modalDescription.innerHTML = `
      <div class="modal-meta-grid">
        <div class="meta-item">
          <span class="meta-label">Product Code:</span>
          <span class="meta-val">${product.id}</span>
        </div>
        <div class="meta-item">
          <span class="meta-label">Category:</span>
          <span class="meta-val">${product.category}</span>
        </div>
        <div class="meta-item">
          <span class="meta-label">Material:</span>
          <span class="meta-val">${product.material}</span>
        </div>
        <div class="meta-item">
          <span class="meta-label">Catalogue Page:</span>
          <span class="meta-val">Page ${product.pageNumber}</span>
        </div>
      </div>

      <p class="modal-desc-text">${product.description}</p>

      ${modelsList}
      ${featuresList}
      ${finishesList}
    `;
  }

  if (modalWhatsApp) {
    const waText = `Hello Vinayak Locks,\\n\\nI am interested in:\\nProduct: ${product.name}\\nCode: ${product.id}\\nCategory: ${product.category}\\nModels: ${product.modelSummary}\\nMaterial: ${product.material}\\n\\nPlease provide official quotation and dealer availability.`;
    modalWhatsApp.href = "https://wa.me/919219609700?text=" + encodeURIComponent(waText);
  }

  if (modal) modal.classList.add("active");
  document.body.style.overflow = "hidden";
}

function closeModal() {
  if (modal) modal.classList.remove("active");
  document.body.style.overflow = "";
}

window.openProduct = openProduct;
window.closeModal = closeModal;
window.selectChip = selectChip;
window.filterByCategory = filterByCategory;
window.clearSearch = clearSearch;
window.resetFilters = resetFilters;

/* SCROLL REVEAL INTERSECTION OBSERVER */
let observer;

function initScrollObserver() {
  if ("IntersectionObserver" in window) {
    observer = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          entry.target.classList.add("active");
          // Once animated, unobserve for max performance
          observer.unobserve(entry.target);
        }
      });
    }, {
      root: null,
      rootMargin: "0px 0px -40px 0px",
      threshold: 0.1
    });

    document.querySelectorAll(".reveal").forEach(el => {
      observer.observe(el);
    });
  } else {
    // Fallback if IntersectionObserver not supported
    document.querySelectorAll(".reveal").forEach(el => {
      el.classList.add("active");
    });
  }
}

function initCardObserver() {
  if (observer) {
    document.querySelectorAll(".product-card.reveal:not(.active)").forEach(card => {
      observer.observe(card);
    });
  } else {
    document.querySelectorAll(".product-card.reveal").forEach(card => {
      card.classList.add("active");
    });
  }
}

/* EVENT LISTENERS */
document.addEventListener("DOMContentLoaded", function () {
  if (searchInput) {
    searchInput.addEventListener("input", renderProducts);
  }

  if (categoryFilter) {
    categoryFilter.addEventListener("change", function () {
      selectChip(this.value);
    });
  }

  const modalClose = document.getElementById("modalClose");
  if (modalClose) {
    modalClose.addEventListener("click", closeModal);
  }

  if (modal) {
    modal.addEventListener("click", function (e) {
      if (e.target === modal) {
        closeModal();
      }
    });
  }

  // Escape key to close modal
  document.addEventListener("keydown", function (e) {
    if (e.key === "Escape" && modal && modal.classList.contains("active")) {
      closeModal();
    }
  });

  const menuToggle = document.getElementById("menuToggle");
  const mainNav = document.getElementById("mainNav");

  if (menuToggle && mainNav) {
    menuToggle.addEventListener("click", function () {
      const opened = mainNav.classList.toggle("active");
      menuToggle.setAttribute("aria-expanded", opened);
    });

    mainNav.querySelectorAll("a").forEach(link => {
      link.addEventListener("click", function () {
        mainNav.classList.remove("active");
        menuToggle.setAttribute("aria-expanded", "false");
      });
    });

    window.addEventListener("resize", function () {
      if (window.innerWidth > 820) {
        mainNav.classList.remove("active");
        menuToggle.setAttribute("aria-expanded", "false");
      }
    });
  }

  const quoteForm = document.getElementById("quoteForm");
  if (quoteForm) {
    quoteForm.addEventListener("submit", function (e) {
      e.preventDefault();

      const name = document.getElementById("name") ? document.getElementById("name").value : "";
      const phone = document.getElementById("phone") ? document.getElementById("phone").value : "";
      const product = document.getElementById("product") ? document.getElementById("product").value : "";
      const message = document.getElementById("message") ? document.getElementById("message").value : "";

      const text = `Hello Vinayak Locks,\\n\\nName: ${name}\\nPhone: ${phone}\\nProduct: ${product}\\nRequirement: ${message}`;

      const url = "https://wa.me/919219609700?text=" + encodeURIComponent(text);
      window.open(url, "_blank");
    });
  }

  renderProducts();
  initScrollObserver();
});

if (document.readyState === "interactive" || document.readyState === "complete") {
  renderProducts();
  initScrollObserver();
}
"""

with open("index.js", "w", encoding="utf-8") as f:
    f.write(js_template)

print("Generated modern index.js successfully!")
