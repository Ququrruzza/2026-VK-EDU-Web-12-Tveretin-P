const csrfToken = document.querySelector('meta[name="csrf-token"]').content;
const loginUrl = document.body.dataset.loginUrl;

// отправляет POST и возвращает JSON, либо null если была ошибка (она уже показана пользователю)
async function sendPost(url, data) {
    let response;
    try {
        response = await fetch(url, {
            method: "POST",
            headers: {"X-CSRFToken": csrfToken},
            body: new URLSearchParams(data),
        });
    } catch (error) {
        alert("Не удалось связаться с сервером. Проверьте подключение.");
        return null;
    }

    if (response.status === 401) {
        window.location.href = loginUrl + "?next=" + encodeURIComponent(location.pathname + location.search);
        return null;
    }
    if (response.status === 403) {
        alert("Запрос отклонён (CSRF). Обновите страницу и попробуйте ещё раз.");
        return null;
    }
    if (response.status === 405) {
        alert("Неверный метод запроса.");
        return null;
    }

    let result;
    try {
        result = await response.json();
    } catch (error) {
        alert("Ошибка сервера, попробуйте позже.");
        return null;
    }
    if (!response.ok) {
        alert(result.error || "Что-то пошло не так.");
        return null;
    }
    return result;
}

// лайки и дизлайки вопросов и ответов
document.querySelectorAll(".js-vote").forEach((button) => {
    button.addEventListener("click", async () => {
        const rating = button.closest(".rating");
        const result = await sendPost(rating.dataset.url, {
            [rating.dataset.field]: rating.dataset.id,
            value: button.dataset.value,
        });
        if (!result) {
            return;
        }

        rating.querySelector(".rating-count").textContent = result.rating;
        const [likeButton, dislikeButton] = rating.querySelectorAll(".js-vote");
        likeButton.disabled = result.value === 1;
        likeButton.classList.toggle("btn-success", result.value === 1);
        likeButton.classList.toggle("btn-outline-success", result.value !== 1);
        dislikeButton.disabled = result.value === -1;
        dislikeButton.classList.toggle("btn-danger", result.value === -1);
        dislikeButton.classList.toggle("btn-outline-danger", result.value !== -1);
    });
});

// отметка правильного ответа
document.querySelectorAll(".js-correct").forEach((checkbox) => {
    checkbox.addEventListener("change", async () => {
        const result = await sendPost(checkbox.dataset.url, {
            question: checkbox.dataset.question,
            answer: checkbox.dataset.answer,
        });
        if (!result) {
            checkbox.checked = !checkbox.checked;
            return;
        }

        document.querySelectorAll(".js-correct").forEach((other) => {
            other.checked = false;
            other.closest(".card").classList.remove("border-success");
        });
        checkbox.checked = result.is_correct;
        checkbox.closest(".card").classList.toggle("border-success", result.is_correct);
    });
});
