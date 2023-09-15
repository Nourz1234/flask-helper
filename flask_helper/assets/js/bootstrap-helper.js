function bsEnsureAlertsContainer() {
    let container = document.querySelector("#bsAlertsContainer");
    if (!container) {
        let html = `
        <div class="container-fluid fixed-top vstack gap-3 p-3 pe-none" id="bsAlertsContainer">
        </div>
        `;
        document.body.insertAdjacentHTML("beforeend", html);
    }
}

function bsAlert(message, category, timeout) {
    category = category || "success";
    timeout = timeout || null;

    bsEnsureAlertsContainer();

    let html = `
    <div class="alert alert-${category} alert-dismissible fade show m-0 ms-auto pe-auto" role="alert">
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
    </div>
    `;
    let element = createElementFromHTML(html);
    document.querySelector("#bsAlertsContainer").insertAdjacentElement(
        "afterbegin", element
    );
    if (timeout != null) {
        setTimeout(
            () => element.querySelector(".btn-close").click(),
            timeout * 1000
        );
    }
}

function bsResetFormErrors(form) {
    for (let input of getFormInputs(form)) {
        if (!input.name)
            continue;
        let errorsContainer = form.querySelector(`[data-feedback-for="${input.name}"]`);
        if (errorsContainer)
            errorsContainer.innerHTML = '';
    }
    form.querySelector('[data-feedback-for="form"]').innerHTML = '';
}

function bsSetFormErrors(form, errors) {
    for (let [input_name, input_errors] of Object.entries(errors)) {
        let input = form.elements.namedItem(input_name);
        if (input) {
            input.setCustomValidity(input_errors.map(x => '-' + x).join("\n"));
            resetInputValidityOnChange(input);
        }
        let errorsContainer = form.querySelector(`[data-feedback-for="${input_name}"]`);
        if (!errorsContainer) {
            errorsContainer = form.querySelector('[data-feedback-for="form"]');
        }
        errorsContainer.insertAdjacentHTML("beforeend", formatThemErrorsForMeDaddy(input_errors));
    }
}

async function bsFormSubmit(form, event, successHandler) {
    event.preventDefault();
    event.stopPropagation()

    form.classList.add('was-validated');
    if (!form.checkValidity()) {
        return;
    }

    let requestSuccessful = false;
    try {
        setFormBusy(form, true);
        bsResetFormErrors(form);

        await sleep(500);
        let formData = null;
        if (form.enctype == "multipart/form-data")
            formData = new FormData(form);
        else if (form.enctype == "application/x-www-form-urlencoded")
            formData = new URLSearchParams(new FormData(form).entries());
        let response = await fetch(form.action, {
            method: form.elements["form_method"].value,
            body: formData,
        });
        let responseData = await response.json();

        if (response.status == 200) {
            requestSuccessful = true;
            if (successHandler) {
                runWithContext(successHandler, { target: form, args: [form, responseData] });
            }
            else {
                bsAlert("Success", "success", 5);
            }
        }
        else if (response.status == 400 && responseData.description === "Validation error.") {
            bsSetFormErrors(form, responseData.errors);
        }
        else {
            bsAlert(responseData.description, "danger", 5);
        }
    }
    catch (err) {
        console.error(err);
        if (requestSuccessful)
            bsAlert("Your form was handled successfully but a client side error has occurred.", "warning", 5);
        else
            bsAlert("Something went wrong.", "danger", 5);

    }
    finally {
        setFormBusy(form, false);
    }
}


function getFormInputs(form) {
    return Array.from(form.elements);
}

function resetInputValidityOnChange(input) {
    let handler = function () {
        input.removeEventListener("change", handler);
        input.removeEventListener("input", handler);
        input.setCustomValidity('');
    }
    input.addEventListener("change", handler);
    input.addEventListener("input", handler);
}

function formatThemErrorsForMeDaddy(errors) {
    items = errors.map(x => `<li>${x}</li>`).join("");
    return `<ul class="m-0">${items}</ul>`;
}

function setFormBusy(form, busy) {
    form.style.opacity = busy ? "0.5" : "1";
    form.style.pointerEvents = busy ? "none" : "auto";
}
