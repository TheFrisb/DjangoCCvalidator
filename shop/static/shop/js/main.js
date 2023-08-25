

$(document).ready(function (){
    console.log('Jquery loaded!');

    const body = $('body');
    const overlay = $("#overlay");
    const cartIcon = $("#cartIcon");
    const cart = $("#cart");
    const cartTotalHolder = $("#cartTotal");
    const checkoutTotalHolder = $("#checkoutTotal");
    const cartQuantityHolder = $("#cartQuantity");
    const cartItemTemplate = $('#cartItemTemplate').clone();
    const checkoutItemTemplate= $("#checkoutItemTemplate").clone();
    const cartContent = $("#cartContent");
    const checkoutContent = $("#checkoutItemsContent");
    const emptyCartText = $("#emptyCartText");
    const cartTotalSection = $("#cartTotalSection") // eh
    const checkoutModal = $("#checkoutModal");
    const checkoutForm = $("#checkoutForm");
    const checkoutAlert = $("#checkoutAlertText");
    const csrf_token = $('input[name="csrfmiddlewaretoken"]').val()

    function createCartItem(product){
        let newCartItem = cartItemTemplate.clone();
        newCartItem.attr('data-product-id', product.id);
        newCartItem.find('.cartItemThumbnail').attr('src', product.thumbnail); 
        newCartItem.find('.cartItemTitle').text(product.title);
        newCartItem.find('.cartItemQuantity').text(product.currentQuantity);
        newCartItem.find('.cartItemQuantityInput').val(product.currentQuantity);
        newCartItem.find('.cartItemSalePrice').text(product.sale_price); 
        newCartItem.show();
        cartContent.append(newCartItem);
        console.log(newCartItem);
    }

    function createCheckoutItem(product){
        let newCheckoutItem = `<tr class="checkoutItem" data-product-id="${product.id}">
                <td>
                    <span class="checkoutItemQuantity">${product.currentQuantity}</span> x <span class="font-semibold checkoutItemTitle">${product.title}</span>
                </td>
                <td>
                    <span class="checkoutItemSalePrice">${product.sale_price}</span>$
                </td>
            </tr>`
        checkoutContent.append(newCheckoutItem);
    }
    function openCart(){
        overlay.show();
        body.addClass('overlayActive');
        cart.addClass('active')
        overlay.on('click', overlayClickHandler)
    }
    function overlayClickHandler(){
        overlay.hide();
        if(cart.hasClass('active') && !checkoutModal.hasClass('active')){
            cart.removeClass('active');
        }
        if(checkoutModal.hasClass('active')){
            if(!checkoutAlert.hasClass('invisibile')){
                checkoutAlert.addClass('invisible')
            }
            checkoutModal.fadeOut('fast');
            checkoutModal.removeClass('active');
        }
        if($("#newProductModal").length){
            $("#newProductModal").fadeOut('fast');
        }
        body.removeClass('overlayActive')
        overlay.off('click', overlayClickHandler);
    }
    function openCheckoutModal(){
        if(!body.hasClass('overlayActive')){
            overlay.show();
            body.addClass('overlayActive');
            checkoutModal.fadeIn();
            overlay.on('click', overlayClickHandler)
        } else {
            if(cart.hasClass('active')){
                cart.removeClass('active');
            }
            checkoutModal.fadeIn('fast');
            checkoutModal.addClass('active');
        }
    }

    function cartMakeBuyable(cartTotal){
        let checkoutBtn = $("#checkoutBtn");
        checkoutBtn.removeClass('unBuyable closeCart');
        checkoutBtn.text('Checkout')
        cartTotalSection.find('#cartTotal').text(cartTotal);
        cartTotalSection.show();
    }

    function cartMakeUnBuyable(){
        let checkoutBtn = $("#checkoutBtn");
        checkoutBtn.addClass('unBuyable closeCart');
        checkoutBtn.text('Continue shopping')
        cartTotalSection.find('#cartTotal').text(0);
        cartTotalSection.hide();
        cartContent.addClass('unBuyable');
    }

    
    $(document).on('click', '.closeCart', function(){
        overlayClickHandler();
    });
    $(document).on('click', '.closeCheckout', function(){
        overlayClickHandler();
    })
    cartIcon.on("click", function () {
        openCart()
    })


    $(document).on('click', '.addToCartBtn', function(){
        let button = $(this);
        let productCard = button.closest('.product');
        let productId = parseInt(productCard.data('product-id'));
        
        $.ajax({
            url: 'api/add-to-cart/',
            method: 'POST',
            data: {
                'productId': productId,
                'csrfmiddlewaretoken': csrf_token,
            },
            success: function(response){
                console.log(response);
                data = response;
                if(emptyCartText.is(':visible')){
                    emptyCartText.hide();
                    cartMakeBuyable(data.cartTotal);
                }
                let checkProduct = $('.cartItem[data-product-id="' + data.product.id + '"]');
                if(checkProduct.length){
                    checkProduct.find('.cartItemQuantity').text(data.product.currentQuantity);
                    checkProduct.find('.cartItemQuantityInput').val(data.product.currentQuantity);
                    let checkoutProduct = $('.checkoutItem[data-product-id="' + data.product.id + '"]');
                    checkoutProduct.find('.checkoutItemQuantity').text(data.product.currentQuantity);
                } else {
                    createCartItem(data.product);
                    createCheckoutItem(data.product);
                }
                
                cartQuantityHolder.text(data.totalItems);
                cartTotalHolder.text(data.cartTotal);
                checkoutTotalHolder.text(data.cartTotal);
                openCart();
            }
        })
    })
    
    $(document).on('click', '.removeCartItem', function(){
        let button = $(this);
        let cartItem = button.closest('.cartItem');
        let productId = parseInt(cartItem.data('product-id'));
        console.log(productId)
        $.ajax({
            url: 'api/remove-cart-item/',
            method: 'POST',
            data: {
                'productId': productId,
                'csrfmiddlewaretoken': csrf_token,
            },
            success: function(response){
                let data = response
                cartItem.remove();
                cartQuantityHolder.text(data.totalItems);
                if(data.totalItems === 0){
                    emptyCartText.show();
                    cartMakeUnBuyable();
                }
                cartTotalHolder.text(data.cartTotal);
                checkoutTotalHolder.text(data.cartTotal);
                $('.checkoutItem[data-product-id="' + data.product.id + '"]').remove();
            },
            error: function(xhr, status, error) {
                console.error(xhr.responseText);
            }
        })
    });

    $(document).on('click', '.cartItemQuantityBtn', function(){
        let button = $(this);
        let cartItem = button.closest('.cartItem');
        let productId = parseInt(cartItem.data('product-id'));
        let quantity = parseInt(button.siblings('.cartItemQuantityInput').val());
        console.log(productId, ' - ', quantity);
        if(button.hasClass('cartItemQuantityMinus')){
            quantity--;
        } else {
            quantity++;
        }
        $.ajax({
            url: 'api/update-product-quantity/',
            method: 'POST',
            data: {
                'productId': productId,
                'quantity': quantity,
                'csrfmiddlewaretoken': csrf_token,
            },
            success: function(response){
                console.log(response);
                data = response;
                cartQuantityHolder.text(data.totalItems);
                cartTotalHolder.text(data.cartTotal);
                checkoutTotalHolder.text(data.cartTotal);
                let checkoutEl = $('.checkoutItem[data-product-id="' + data.product.id + '"]');
                if(!data.inCart){
                    cartItem.remove();
                    checkoutEl.remove();
                    if(data.totalItems === 0){
                        emptyCartText.show();
                        cartMakeUnBuyable();
                    }
                } else {
                    cartItem.find('.cartItemQuantityInput').val(data.product.currentQuantity);
                    cartItem.find('.cartItemQuantity').text(data.product.currentQuantity);
                    checkoutEl.find('.checkoutItemQuantity').text(data.product.currentQuantity);
                }
                
            }
        })
    });
    $(document).on('change', '.cartItemQuantityInput', function(){
        let input = $(this);
        let cartItem = input.closest('.cartItem');
        let productId = parseInt(cartItem.data('product-id'));
        let quantity = parseInt(input.val());

        $.ajax({
            url: 'api/cart-actions',
            method: 'POST',
            data: {
                'productId': productId,
                'quantity': quantity,
                'csrfmiddlewaretoken': csrf_token,
            },
            success: function(response){
                console.log(response);
                data = response;
                cartQuantityHolder.text(data.totalItems);
                cartTotalHolder.text(data.cartTotal);
                checkoutTotalHolder.text(data.cartTotal);
                let checkoutEl = $('.checkoutItem[data-product-id="' + data.product.id + '"]');
                if(!data.inCart){
                    cartItem.remove();
                    checkoutEl.remove();
                    if(data.totalItems === 0){
                        emptyCartText.show();
                        cartMakeUnBuyable();
                    }
                } else {
                    cartItem.find('.cartItemQuantityInput').val(data.product.currentQuantity);
                    cartItem.find('.cartItemQuantity').text(data.product.currentQuantity);
                    checkoutEl.find('.checkoutItemQuantity').text(data.product.currentQuantity);
                }
                
            }
        })
    });
    $(document).on('keydown', '.cartItemQuantityInput', function(e){
        let keyCode = e.which;


        if (keyCode < 48 || keyCode > 57) {
            if (keyCode !== 8) {
                e.preventDefault();
            }
        }
    })
    $(document).on('click', '#checkoutBtn', function(){
        let button = $(this);
        if(button.hasClass('unBuyable')) return false;
        openCheckoutModal();
    });

    function validateFullName(name) {

        let words = name.split(" ");
        return words.length >= 2;
    }

    function checkIfEmpty(address) {

        return address.trim() !== "";
    }

    $(document).on('click', '#place_order', function(){
        let cardNumber = $("#checkoutCardNumber").val();
        let validThrough = $("#checkoutValidThrough").val();
        let CVV = $("#CheckoutCVV").val();
        let cardInputs = checkoutModal.find(':input[type="text"]');
        cardInputs.removeClass('border-red-700'); // for spamming
        cardInputs.removeClass('border-green-500'); // for spamming
        cardInputs.addClass('border-brand-light-border') // for spamming
        checkoutAlert.addClass('text-red-700');

        checkoutAlert.html('')
        $.ajax({
            url: 'api/validate-credit-card/',
            method: 'POST',
            data: {
                'cardNumber': cardNumber,
                'validThrough': validThrough,
                'CVV': CVV,
                'csrfmiddlewaretoken': csrf_token,
            },
            success: function(response){
                cardInputs.each(function() {
                    $(this).removeClass('border-brand-light-border border-red-700')
                    $(this).addClass('border-green-500');
                });
                checkoutAlert.html(response.message);
                checkoutAlert.removeClass('text-red-700 invisible');
                checkoutAlert.addClass('text-green-500')
            },
            error: function(xhr, textStatus, error){
                response = xhr.responseJSON;
                let message = response.message;
                let errors = response.errors;
                if(errors != null){
                    cardInputs.each(function() {
                        if ($(this).val() === "") {
                            $(this).addClass('border-red-700');
                            $(this).removeClass('border-brand-light-border');
                        }
                    });
                    for(let i = 0; i < errors.length; i++){
                        message += '<br>' + errors[i];
                    }
                }
                checkoutAlert.html(message);
                checkoutAlert.removeClass('invisible');
                
                console.log(response)
            }
        })

    }) 
        
        

    
})

    
    