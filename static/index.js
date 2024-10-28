function addPost(title,description,id,likedByUser,likeCount) {
    let template = document.getElementById("postTemplate")
    let html = template.content.cloneNode(true)
    html.querySelector(".title").innerHTML=title
    html.querySelector(".description").innerHTML=description
    html.querySelector(".likeCount").innerHTML=likeCount
    if(likedByUser){
        html.querySelector(".likeButton").classList.add("liked")
    }
    document.getElementById("posts").appendChild(html)
    //find delete button on newest item and add event listener to delete its parent
    let likeButton = document.querySelectorAll(".likeButton")
    likeButton=likeButton[likeButton.length-1]
    likeButton.addEventListener("click", _ => {
        let formData = new FormData();
        formData.append("postID",id)
        fetch("/likePost",{
            method:"post",
            body: formData
        })
        setTimeout(getPosts,100)
    })
}
function getPosts(){
    fetch("/post")
        .then(res=>res.json())
        .then(json=>{
            document.querySelector("#posts").innerHTML=""
            json[1].forEach(post => {
                let likedByUser=false
                post.reactions.forEach(reaction=>{
                    if(reaction.username==json[0]){
                        likedByUser=true
                    }
                })
                addPost(post.title,post.description,post._id.$oid,likedByUser,post.reactions.length)
            });
        })
}

let form=document.getElementById("postForm");

//Calling a function during form submission.
form.addEventListener('submit', makePost);
function makePost(event){
    fetch("/post",{
        method:"post",
        body: new FormData(form)
    })
    event.preventDefault();
    getPosts()
}
getPosts()
setInterval(getPosts,5000)