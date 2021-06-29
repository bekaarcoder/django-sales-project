const modalBody = document.querySelector("#modal-body");
const reportBtn = document.querySelector("#report-btn");
const chartImg = document.querySelector("#chart-img");

const reportName = document.querySelector("#id_name");
const reportRemarks = document.querySelector("#id_remarks");
const csrf = document.getElementsByName("csrfmiddlewaretoken")[0].value;
const reportForm = document.querySelector("#report-form");

reportBtn.addEventListener("click", () => {
    chartImg.setAttribute("class", "img-fluid");
    modalBody.prepend(chartImg);
});

reportForm.addEventListener("submit", (e) => {
    e.preventDefault();
    const formData = new FormData();
    formData.append("csrfmiddlewaretoken", csrf);
    formData.append("name", reportName.value);
    formData.append("remarks", reportRemarks.value);
    formData.append("image", chartImg.src);

    fetch("/reports/create/", {
        method: "POST",
        body: formData,
    })
        .then((res) => res.json())
        .then((data) => console.log(data));
});
