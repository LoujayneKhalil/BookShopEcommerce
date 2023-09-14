function getCartFromLocalStorage() {
  const cart = localStorage.getItem("cart");
  return cart ? JSON.parse(cart) : [];
}

function updateCartInLocalStorage(cart) {
  localStorage.setItem("cart", JSON.stringify(cart));
}

let guestCart = getCartFromLocalStorage();

var updateBtns = document.getElementsByClassName("update-cart");

function updateCartItemCount() {
  const cartItemCountElement = document.getElementById("cartItemCount");
  const cartItemCount = guestCart.length;
  cartItemCountElement.textContent = cartItemCount;
}

updateCartItemCount();

var updateBtns = document.getElementsByClassName("update-cart");

for (i = 0; i < updateBtns.length; i++) {
  // console.log("How many rendered")
  updateBtns[i].addEventListener("click", function () {
    var productID = this.dataset.product;
    console.log("productID: ", productID);
    addProductToCartForAuthenticatedUser(productID);
  });
}

function addProductToCartForAuthenticatedUser(productID) {
  // Add product to local storage
  const productName = document
    .querySelector(`[data-product="${productID}"]`)
    .getAttribute("data-name");
  const productPrice = parseFloat(
    document
      .querySelector(`[data-product="${productID}"]`)
      .getAttribute("data-price")
  );
  let cartItem = {
    product_id: productID,
    name: productName,
    price: productPrice,
    quantity: 1,
  };
  let guestCart = getCartFromLocalStorage();

  console.log("is cart?? ", guestCart);

  let found = false;
  guestCart.forEach((prod) => {
    if (prod.product_id === productID) {
      prod.quantity += 1;
      console.log("how many times", prod.product_id, productID);
      found = true;
    }
  });
  if (!found) {
    console.log("Found?");
    guestCart.push(cartItem);
  } else {
    found = false;
  }
  updateCartInLocalStorage(guestCart);
  location.reload();
}

var test = getCartFromLocalStorage();
$(".btn-place-order").click(function () {
  const csrfToken = document.querySelector(
    'input[name="csrfmiddlewaretoken"]'
  ).value;

  cart_data = {
    cart_products: getCartFromLocalStorage(),
    total_amount: 0,
  };
  console.log("token  ", csrfToken);
  console.log("user??? ", user);
  if ("{{ user.is_authenticated }}") {
    console.log("authenticated?  ");
    const request = new Request("/place_order/", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "X-CSRFToken": csrfToken,
      },
      body: JSON.stringify(cart_data),
    });

    //Fetch function
    fetch(request)
      .then((response) => {
        if (!response.ok) {
          throw new Error("Network response was not ok");
        }
        localStorage.removeItem("cart");
        window.location.href = response.url;
      })
      .then((data) => {
        console.log("Response from server:", data);
      })
      .catch((error) => {
        console.error("Fetch error:", error);
      });
  }
});

const EmptyCartElement = document.querySelector(".table-box");
const CartShippingElement = document.querySelector("cart_shipping");

$(document).ready(function () {
  function displayGuestCart() {
    const guestCart = JSON.parse(localStorage.getItem("cart"));

    if (!guestCart || guestCart.length === 0) {
      $(".table-box").html(
        '<p class="text-center empty-cart">The Cart is Empty</p>'
      );
      $(".order-payment").css("display", "none");
      return;
    }

    let guestCartSubtotal = 0;
    console.log("array ", guestCart);
    guestCart.map((product) => {
      guestCartSubtotal += product.price * product.quantity;

      $(".prod").append(`
        <tr>
            <td>${product.name}</td>
            <td>EGP ${product.price}</td>
            <td>
            <button class="plus-minus minus-btn" data-product="${
              product.product_id
            }">-</button>
            <span class="quantity">${product.quantity}</span>
            <button class="plus-minus plus-btn" data-product="${
              product.product_id
            }">+</button>
            </td>
            <td>EGP ${product.price * product.quantity}</td>
            <td class="delete-action">
                <button class="delete-btn" data-product="${
                  product.product_id
                }"><i class="fa-solid fa-trash"></i></button>
            </td>
        </tr>       
        `);
    });

    $(".delete-btn").click(function () {
      const productID = $(this).data("product");
      console.log("productID clicked", productID);
      removeItemFromCart(productID);
    });
    $("#subtotal_value").text(`${guestCartSubtotal.toFixed(2)}`);
    const shippingFee = 40;
    const total = guestCartSubtotal + shippingFee;
    $("#total_price").text(`Total: EGP ${total.toFixed(2)}`);

    function removeItemFromCart(productID) {
      let guestCart = getCartFromLocalStorage();
      console.log("guestCart:", guestCart);
      console.log("productID to find:", productID);

      const itemIndex = guestCart.findIndex(
        (product) => product.product_id === `${productID}`
      );

      if (itemIndex !== -1) {
        guestCart.splice(itemIndex, 1);
        updateCartInLocalStorage(guestCart);
      }
      location.reload();
    }
    $(".plus-btn").click(function () {
        const productID = $(this).data("product");
        console.log(productID);
      incrementQuantity(productID);
    });

    $(".minus-btn").click(function () {
      const productID = $(this).data("product");
      console.log(productID);
      decrementQuantity(productID);
    });
    function incrementQuantity(productID) {
      let guestCart = getCartFromLocalStorage();
    //   console.log(guestCart);

    const itemIndex = guestCart.findIndex(
        (product) => product.product_id === `${productID}`
      );
      console.log("Item:",itemIndex);

      if (itemIndex !== -1) {
        guestCart[itemIndex].quantity += 1;
        updateCartInLocalStorage(guestCart);
      } else {
        console.log("Product not found in the cart:", productID);
      }
      location.reload()
    }

    function decrementQuantity(productID) {
        let guestCart = getCartFromLocalStorage();
      
        const itemIndex = guestCart.findIndex(
            (product) => product.product_id === `${productID}`
            );
            console.log(itemIndex)
        if (itemIndex !== -1 && guestCart[itemIndex].quantity > 1) {
            console.log("not equal to 1")
          guestCart[itemIndex].quantity -= 1;
          updateCartInLocalStorage(guestCart);
        }
        location.reload()
      }

  }
  displayGuestCart();
});
