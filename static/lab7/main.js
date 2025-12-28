let editId = null;

function fillFilmList() {
    fetch('/lab7/rest-api/films/')
        .then(r => r.json())
        .then(films => {
            let tbody = document.getElementById('film-list');
            tbody.innerHTML = '';

            for (let i = 0; i < films.length; i++) {
                let tr = document.createElement('tr');

                tr.innerHTML = `
                    <td>${films[i].title}</td>
                    <td>${films[i].title_ru}</td>
                    <td>${films[i].year}</td>
                    <td>
                        <button onclick="editFilm(${i})">Редактировать</button>
                        <button onclick="deleteFilm(${i})">Удалить</button>
                    </td>
                `;
                tbody.appendChild(tr);
            }
        });
}

function saveFilm() {
    let film = {
        title: document.getElementById('title').value,
        title_ru: document.getElementById('title_ru').value,
        year: Number(document.getElementById('year').value),
        description: document.getElementById('description').value
    };

    let url = '/lab7/rest-api/films/';
    let method = 'POST';

    if (editId !== null) {
        url += editId;
        method = 'PUT';
    }

    fetch(url, {
        method: method,
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify(film)
    }).then(() => {
        editId = null;
        clearForm();
        fillFilmList();
    });
}

function editFilm(id) {
    fetch(`/lab7/rest-api/films/${id}`)
        .then(r => r.json())
        .then(film => {
            editId = id;
            document.getElementById('title').value = film.title;
            document.getElementById('title_ru').value = film.title_ru;
            document.getElementById('year').value = film.year;
            document.getElementById('description').value = film.description;
        });
}

function deleteFilm(id) {
    fetch(`/lab7/rest-api/films/${id}`, { method: 'DELETE' })
        .then(() => fillFilmList());
}

function clearForm() {
    document.getElementById('title').value = '';
    document.getElementById('title_ru').value = '';
    document.getElementById('year').value = '';
    document.getElementById('description').value = '';
}
