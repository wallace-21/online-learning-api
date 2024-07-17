document.addEventListener('DOMContentLoaded', () => {
    const loadButton = document.getElementById('loadEndpoint');
    const createButton = document.getElementById('createData');
    const updateButton = document.getElementById('updateData');
    const deleteButton = document.getElementById('deleteData');
    const endpointInput = document.getElementById('endpoint');
    const jsonInput = document.getElementById('jsonInput');
    const resultContainer = document.getElementById('result');

    const baseURL = 'http://127.0.0.1:5000/';

    loadButton.addEventListener('click', () => {
        const endpoint = endpointInput.value;
        fetch(`${baseURL}${endpoint}`)
            .then(response => response.json())
            .then(data => {
                resultContainer.innerHTML = `<pre>${JSON.stringify(data, null, 2)}</pre>`;
            })
            .catch(error => {
                resultContainer.innerHTML = `<p>Error: ${error.message}</p>`;
            });
    });

    createButton.addEventListener('click', () => {
        const endpoint = endpointInput.value;
        const jsonData = jsonInput.value;

        try {
            const data = JSON.parse(jsonData);
            fetch(`${baseURL}${endpoint}`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(data)
            })
                .then(response => response.json())
                .then(data => {
                    resultContainer.innerHTML = `<pre>${JSON.stringify(data, null, 2)}</pre>`;
                })
                .catch(error => {
                    resultContainer.innerHTML = `<p>Error: ${error.message}</p>`;
                });
        } catch (error) {
            resultContainer.innerHTML = `<p>Invalid JSON: ${error.message}</p>`;
        }
    });

    updateButton.addEventListener('click', () => {
        const endpoint = endpointInput.value;
        const jsonData = jsonInput.value;

        try {
            const data = JSON.parse(jsonData);
            fetch(`${baseURL}${endpoint}`, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(data)
            })
                .then(response => response.json())
                .then(data => {
                    resultContainer.innerHTML = `<pre>${JSON.stringify(data, null, 2)}</pre>`;
                })
                .catch(error => {
                    resultContainer.innerHTML = `<p>Error: ${error.message}</p>`;
                });
        } catch (error) {
            resultContainer.innerHTML = `<p>Invalid JSON: ${error.message}</p>`;
        }
    });

    deleteButton.addEventListener('click', () => {
        const endpoint = endpointInput.value;
        fetch(`${baseURL}${endpoint}`, {
            method: 'DELETE'
        })
            .then(response => response.json())
            .then(data => {
                resultContainer.innerHTML = `<pre>${JSON.stringify(data, null, 2)}</pre>`;
            })
            .catch(error => {
                resultContainer.innerHTML = `<p>Error: ${error.message}</p>`;
            });
    });
});
