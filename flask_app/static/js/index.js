function increaselikes(event){
    console.log(event);
    let currentButton = event.target;
    let numberLikes = parseInt(currentButton.closest('.likes_count').querySelector('.numberLikes').textContent);
    numberLikes += 1;
    currentButton.closest('.likes_count').querySelector('.numberLikes').textContent = numberLikes;
}

let likeButton = document.querySelectorAll('.likelink');
for(let i = 0; i < likeButton.length; i++){
    likeButton[i].addEventListener("click", increaselikes);
}

function alertFunction() {
    alert("Su cuenta ha sido eliminada exitosamente");
}

