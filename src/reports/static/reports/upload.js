const csrf = document.getElementsByName("csrfmiddlewaretoken")[0].value;
const alertBox = document.querySelector("#alert-box");
const form = document.querySelector("#upload-form");

const handleAlert = (type, message) => {
    alertBox.innerHTML = `<div class='alert alert-${type}'>${message}</div>`;
};

Dropzone.autoDiscover = false;
const dropzone = new Dropzone("#upload-form", {
    url: "/reports/upload/",
    init: function () {
        this.on("sending", function (file, xhr, formData) {
            console.log("sending");
            formData.append("csrfmiddlewaretoken", csrf);
        });
        this.on("success", function (file, response) {
            if (response.exists) {
                handleAlert(
                    "danger",
                    "This file has been already uploaded. Please upload another file."
                );
                form.classList.remove("success-box");
                form.classList.add("error-box");
            } else {
                handleAlert("success", "File has been uploaded successfully.");
                form.classList.remove("error-box");
                form.classList.add("success-box");
            }
        });
    },
    maxFiles: 3,
    maxFilesize: 3,
    acceptedFiles: ".csv",
});
