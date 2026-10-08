// Сворачивание и разворачивание информации о рекламном ролике.
// Компактная реализация: класс folded добавляется родителю поста (.one-post),
// а скрытие элементов выполняется CSS-правилами .one-post.folded ...
var foldBtns = document.getElementsByClassName("fold-button");

for (var i = 0; i < foldBtns.length; i++) {
    foldBtns[i].addEventListener("click", function (e) {
        var post = e.target.closest(".one-post");
        var folded = post.classList.toggle("folded");
        e.target.innerHTML = folded ? "развернуть" : "свернуть";
    });
}