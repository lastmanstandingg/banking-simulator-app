document.addEventListener("DOMContentLoaded", function () {


// =====================================
// 1. SHOW AND HIDE PASSWORD
// =====================================

const passwordFields = document.querySelectorAll(
    'input[type="password"]'
);

passwordFields.forEach(function (field) {

    const toggle = document.createElement("button");

    toggle.type = "button";
    toggle.textContent = "Show";
    toggle.className = "password-toggle";

    field.insertAdjacentElement("afterend", toggle);

    toggle.addEventListener("click", function () {

        if (field.type === "password") {
            field.type = "text";
            toggle.textContent = "Hide";
        } else {
            field.type = "password";
            toggle.textContent = "Show";
        }

    });

});


// =====================================
// 2. VALIDATE BANKING AMOUNTS
// =====================================

const amountFields = document.querySelectorAll(
    'input[name="amount"]'
);

amountFields.forEach(function (field) {

    field.addEventListener("input", function () {

        const amount = Number(field.value);

        if (field.value !== "" && (!Number.isFinite(amount) || amount <= 0)) {
            field.setCustomValidity(
                "Please enter a valid positive amount."
            );
        } else {
            field.setCustomValidity("");
        }

    });

});


// =====================================
// 3. CONFIRM DEPOSITS
// =====================================

const depositForm = document.querySelector(
    'form[action="/deposit"]'
);

if (depositForm) {

    depositForm.addEventListener("submit", function (event) {

        const amount = Number(
            depositForm.querySelector('[name="amount"]').value
        );

        if (amount <= 0 || amount > 1000000) {
            event.preventDefault();
            alert("Please enter a valid deposit amount.");
            return;
        }

        if (!confirm(
            "Are you sure you want to deposit MWK " +
            amount.toLocaleString("en-US") + "?"
        )) {
            event.preventDefault();
        }

    });

}


// =====================================
// 4. CONFIRM WITHDRAWALS
// =====================================

const withdrawForm = document.querySelector(
    'form[action="/withdraw"]'
);

if (withdrawForm) {

    withdrawForm.addEventListener("submit", function (event) {

        const amount = Number(
            withdrawForm.querySelector('[name="amount"]').value
        );

        if (amount <= 0) {
            event.preventDefault();
            alert("Invalid withdrawal amount.");
            return;
        }

        if (!confirm(
            "Confirm withdrawal of MWK " +
            amount.toLocaleString("en-US") + "?"
        )) {
            event.preventDefault();
        }

    });

}


// =====================================
// 5. CONFIRM ACCOUNT TRANSFERS
// =====================================

const transferForm = document.querySelector(
    'form[action="/transfer"]'
);

if (transferForm) {

    transferForm.addEventListener("submit", function (event) {

        const recipient = transferForm.querySelector(
            '[name="recipient_account"]'
        ).value.trim();

        const amount = Number(
            transferForm.querySelector('[name="amount"]').value
        );

        if (!recipient || amount <= 0) {

            event.preventDefault();

            alert("Please provide valid transfer details.");

            return;
        }

        if (!confirm(
            "Confirm virtual transfer?\n\n" +
            "Recipient: " + recipient +
            "\nAmount: MWK " +
            amount.toLocaleString("en-US")
        )) {

            event.preventDefault();

        }

    });

}


// =====================================
// 6. PREVENT MULTIPLE FORM SUBMISSIONS
// =====================================

const bankingForms = document.querySelectorAll(
    'form[action="/deposit"], form[action="/withdraw"], form[action="/transfer"]'
);

bankingForms.forEach(function (form) {

    form.addEventListener("submit", function (event) {

        if (!form.checkValidity()) {
            return;
        }

        const button = form.querySelector(
            'button[type="submit"]'
        );

        if (button && !button.disabled) {

            button.dataset.originalText = button.textContent;

            button.disabled = true;

            button.textContent = "Processing...";

        }

    });

});


// =====================================
// 7. LIVE DIGITAL CLOCK
// =====================================

const clock = document.getElementById("digital-clock");

function updateClock() {

    if (!clock) return;

    const now = new Date();

    clock.textContent = now.toLocaleString();

}

updateClock();

setInterval(updateClock, 1000);


// =====================================
// 8. MOBILE NAVIGATION
// =====================================

const menuButton = document.getElementById("menu-toggle");

const navigation = document.querySelector("nav");

if (menuButton && navigation) {

    menuButton.addEventListener("click", function () {

        navigation.classList.toggle("active");

    });

}


// =====================================
// 9. CONFIRM LOGOUT
// =====================================

const logoutLinks = document.querySelectorAll(
    'a[href="/logout"]'
);

logoutLinks.forEach(function (link) {

    link.addEventListener("click", function (event) {

        if (!confirm("Are you sure you want to logout?")) {

            event.preventDefault();

        }

    });

});


// =====================================
// 10. FORMAT MWK CURRENCY
// =====================================

const currencyElements = document.querySelectorAll(
    ".currency-format"
);

currencyElements.forEach(function (element) {

    const amount = Number(element.textContent);

    if (Number.isFinite(amount)) {

        element.textContent = "MWK " +
            amount.toLocaleString("en-US", {
                minimumFractionDigits: 2,
                maximumFractionDigits: 2
            });

    }

});


// =====================================
// 11. AUTO DISMISS FLASH MESSAGES
// =====================================

const flashMessages = document.querySelectorAll(
    ".flash-message"
);

flashMessages.forEach(function (message) {

    setTimeout(function () {

        message.style.opacity = "0";

        setTimeout(function () {
            message.remove();
        }, 500);

    }, 5000);

});


// =====================================
// 12. TRANSACTION SEARCH
// =====================================

const searchInput = document.getElementById(
    "transaction-search"
);

const transactionRows = document.querySelectorAll(
    ".transaction-row"
);

if (searchInput) {

    searchInput.addEventListener("input", function () {

        const searchValue = searchInput.value.toLowerCase();

        transactionRows.forEach(function (row) {

            const text = row.textContent.toLowerCase();

            row.style.display = text.includes(searchValue)
                ? ""
                : "none";

        });

    });

}


// =====================================
// 13. ADMIN CUSTOMER SEARCH
// =====================================

const customerSearch = document.getElementById(
    "customer-search"
);

const customerRows = document.querySelectorAll(
    ".customer-row"
);

if (customerSearch) {

    customerSearch.addEventListener("input", function () {

        const value = customerSearch.value.toLowerCase();

        customerRows.forEach(function (row) {

            row.style.display =
                row.textContent.toLowerCase().includes(value)
                    ? ""
                    : "none";

        });

    });

}


console.log("TITA BANK Banking Simulator initialized successfully.");


});
