document.addEventListener("DOMContentLoaded", function() {
    document.getElementById("plagiarism-form").addEventListener("submit", function(event){
        getPlagiarimResult(event);
    });
});


/**
 * 
 * This function creates a new file input field and appends it to the form
 * after the last file input field.
 * 
 * @returns {void}
 * 
 */
function addFileInput(){
    const lastFileInput = document.querySelectorAll(".file-input").item(
        document.querySelectorAll(".file-input").length - 1
    );

    const count = document.querySelectorAll(".file-input").length + 1;

    let label = document.createElement("label");
    label.htmlFor = `file-${count}`;
    label.className = "form-label small";
    label.textContent = `File ${count}`;

    let fileInput = document.createElement("input");
    fileInput.type = "file";
    fileInput.className = "form-control file-inputs";
    fileInput.id = `file-${count}`;
    fileInput.accept = ".py";
    fileInput.required = true;
    fileInput.name = `file-${count}`;

    let inputDiv = document.createElement("div");
    inputDiv.className = "file-input mb-3";
    inputDiv.appendChild(label);
    inputDiv.appendChild(fileInput);
    
    lastFileInput.insertAdjacentElement('afterend',inputDiv);
}


/**
 * 
 * This function deletes from DOM the last file input field.
 * 
 * @returns {void}
 */
function deleteFileInput(){

    const count = document.querySelectorAll(".file-input").length;
    const lastFileInput = document.querySelectorAll(".file-input").item(
        document.querySelectorAll(".file-input").length - 1
    );

    if(count > 2) lastFileInput.remove();
}


/**
 * 
 * This function makes a request to the API to get the plagiarism result
 * and displays it in the DOM.
 * 
 * @param {*} event 
 * 
 * @returns {void}
 */
async function getPlagiarimResult(event){

    event.preventDefault();

    const base_url = "http://localhost:4800";
    const url = `${base_url}/v1.1/process`;
    
    const form = document.querySelector("#plagiarism-form");
    const formData = new FormData(form);

    console.log(formData);

    // Request using fetch API
    let req = await fetch(url, {
        method: 'POST',
        body: formData,
    });

    // Response
    let res = await req.json();

    const report_result = res.report;

    let divResultsContainer = document.querySelector("#results-container");
    divResultsContainer.innerHTML = "";

    // If there are no results display a message
    if(report_result.length == 0){
        const report_div = document.createElement("div");
        report_div.className = "report";
        report_div.innerHTML = `
            <div class="row">
                <div class="col-12">
                    <h5>Report results</h5>
                </div>
            </div>
            <div class="row">
                <div class="col-md-12">
                    <p>No results</p>
                </div>
            </div>
        `;
        divResultsContainer.appendChild(report_div);
    }


    // Create the title of the results
    const resultTtitle = document.createElement("div");

    resultTtitle.className = "row";
    resultTtitle.innerHTML = `
        <div class="col-12">
            <h5>Report results</h5>
        </div>
    `

    divResultsContainer.appendChild(resultTtitle)

    // Create the results for each report and append it to the DOM
    for(let i = 0; i < report_result.length; i++){
        console.log(report_result[i]);
        const report = report_result[i];
        const report_div = document.createElement("div");

        report_div.className = "report";
        report_div.innerHTML = `
            <div class="row">
                <h6 class="mt-4">Reporte ${i + 1}</h6>
                <div class="col-md-6">
                    <p>File 1: ${report.file1}</p>
                </div>
                <div class="col-md-6">
                    <p>File 2: ${report.file2}</p>
                </div>
            </div>
            <div class="row">
                <div class="col-md-12">
                    <div class="progress">
                        <div class="progress-bar" 
                            role="progressbar" 
                            style="width: ${report.similarity}%" 
                            aria-valuenow="${report.similarity}" 
                            aria-valuemin="0" 
                            aria-valuemax="100"
                        >
                            ${(report.similarity).toFixed(2)}%
                        </div>
                    </div>
                </div>
            </div>
        `;
        
        divResultsContainer.appendChild(report_div);
    }
}