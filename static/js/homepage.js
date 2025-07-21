// Get modal elements
const modal = document.getElementById("modal");
const logoCartoon = document.getElementById("logoCartoon");
const closeBtn = document.querySelector(".close");

// Show modal when logo is clicked
logoCartoon.addEventListener("click", () => {
  modal.style.display = "flex"; // Show the modal
});

// Close modal when the 'X' is clicked
closeBtn.addEventListener("click", () => {
  modal.style.display = "none";
});

// Close modal when clicking outside the modal content
window.addEventListener("click", (event) => {
  if (event.target === modal) {
    modal.style.display = "none";
  }
});


 document.querySelector('.bi-cart').addEventListener('click', function () {
     window.location.href = '/cart'; // Redirects to the cart page
  });

