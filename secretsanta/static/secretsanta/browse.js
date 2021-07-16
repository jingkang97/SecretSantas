document.addEventListener('DOMContentLoaded', function() {

  console.log('loaded')
  // by default load the first one
  // get check value
  // load all none first
  // load that check value first


  // get the likes
  li = []

  // below will load the colors of the heart correctly
  var likes = document.getElementById('likes')
  console.log(likes.children)
  for (var t = 0; t < likes.children.length; t++){
    console.log(likes.children[t].getAttribute("id"))
    li.push({user:likes.children[t].getAttribute("user"), gift: likes.children[t].getAttribute("gift"), group: likes.children[t].getAttribute("group")})
  }

  console.log(li)

  var hearts = document.querySelectorAll('.love')

  var user_current = document.getElementById('user')
  console.log(user_current.getAttribute("value"))

  for(var l = 0; l < hearts.length; l++){

    for(var i = 0; i < li.length; i++){
      if(li[i].user == user_current.getAttribute("value") && li[i].gift == hearts[l].getAttribute("gift") && li[i].group == hearts[l].getAttribute("group")){
        hearts[l].style.color = "red"
      }
    }
  }


  groups = document.querySelectorAll('.group')
  for (var j = 0; j < groups.length; j++ ){
    console.log(groups[j])
    groups[j].style.display = 'none'
  }


  var radio_buttons = document.querySelectorAll('.custom-control-input')
  for (var i = 0; i < radio_buttons.length; i++){
    // if check attribute is true
    console.log(radio_buttons[i].checked)
    if(radio_buttons[i].checked){
      show_group(radio_buttons[i].value)
      
    }
  }


});



function show_group(group_id){
  console.log(group_id)

  console.log('hi')
  // make all none first


  var groups = document.querySelectorAll('.group')

  for(var i = 0; i < groups.length; i++){
    groups[i].style.display = 'none'
    console.log(groups[i])
  }

  var nogroups = document.querySelectorAll('.nogroup')

  for(var i = 0; i < nogroups.length; i++){
    nogroups[i].style.display = 'none'
    console.log(nogroups[i])
  }


  // make this one block
  var group = document.querySelector(`#${group_id}`)


  console.log(group)
  group.style.display = 'block'  

}


function edit_notes(wishlist_id){

  console.log(wishlist_id)

  var note = document.getElementById(`${wishlist_id}-edit-note`)
  console.log(note)

  if (note.style.display == 'block'){
    note.style.display = 'none'
  }else{
    note.style.display = 'block'

  }

  
}

function cancel(wishlist_id){
  var note = document.getElementById(`${wishlist_id}-edit-note`)
  console.log(wishlist_id)

  val = document.getElementById(`${wishlist_id}-value`)


  message = document.getElementById(`${wishlist_id}-textarea`)


  console.log(message.value)

  if(val == null){
    message.value = ""
  }else{
    message.value = val.getAttribute('value')
  }


  if (note.style.display == 'block'){


    note.style.display = 'none'
  }else{
    note.style.display = 'block'

  }
}


function delete_panel(like_id,group_id){
  var like_count = document.querySelectorAll(`.likes-${like_id}`)


  fetch(`/like/${like_id}/${group_id}`, {
            method: 'PUT',
            body: JSON.stringify({
                like: false
            })
        }).then(response => {
            fetch(`/like/${like_id}/${group_id}`)
            .then(response => response.json())
            .then(gift => {
                // console.log(gift)
                for(var i = 0; i < like_count.length; i ++){
                  like_count[i].innerHTML = gift.likes
                }
                // console.log(like_count.innerHTML)

            });
        }

        )

    var remove_panel = document.getElementById(`${like_id}-${group_id}-gift-wishlist`)
    remove_panel.remove()

    var like_objects = document.querySelectorAll(`.like-btn-${like_id}-${group_id}`)


        for(var k = 0; k < like_objects.length; k++){
        if( like_objects[k].style.color=="red"){
          like_objects[k].style.color = 'white'
          console.log(like_objects[k])

        }
        
      }
    return false;
}




function like(like_id, group_id){
  
  var wishlist_count = document.getElementById("wish_count")
  console.log(wishlist_count.innerHTML)

  var like_object = document.getElementById(`like-btn-${like_id}-${group_id}`)



  var like_count = document.querySelectorAll(`.likes-${like_id}`)
  
  

  if(like_object.style.color == "white"){
    
    var count = wishlist_count.getAttribute("value")
    console.log(count)
    count ++
    wishlist_count.innerHTML = count
    wishlist_count.setAttribute("value", count)

    var panel = document.createElement("DIV")


    panel.setAttribute("style","border-radius: 20px; margin: 5px; margin-bottom: 10px; width: 100%; height: 100px; display: flex; flex-direction: row; justify-content: space-between; ")

    panel.setAttribute("class","shadow")
    panel.setAttribute("id",`${like_id}-${group_id}-gift-wishlist`)


    var image = document.getElementById(`${like_id}-image`)
    var title = document.getElementById(`${like_id}-title`)
    var price = document.getElementById(`${like_id}-price`)

    console.log(image.src)
    console.log(title.getAttribute('value'))
    console.log(price.getAttribute('value'))


    var image_div = document.createElement("DIV")

    image_div.setAttribute("style","width: 100px; border-top-left-radius: 20px; border-bottom-left-radius: 20px");

    img = document.createElement("IMG")
    img.src = image.src
    img.setAttribute("style","width: 100px; height: 100px; border-top-left-radius: 20px; border-bottom-left-radius: 20px ")

    image_div.appendChild(img)

    var description_div = document.createElement("DIV")
    description_div.setAttribute("style","width: 100%; padding: 20px; display: flex; flex-direction: column; justify-content: center; text-align: center; align-content:center; border-top-right-radius: 20px; border-bottom-right-radius: 20px;")

    var gift_title = document.createElement("H6")
    gift_title.style.color = "grey"
    gift_title.innerHTML = title.getAttribute('value')

    var gift_price = document.createElement("H5")
    gift_price.innerHTML = "$" + price.getAttribute('value')


    description_div.appendChild(gift_title)
    description_div.appendChild(gift_price)


    cross_div = document.createElement("DIV")
    cross_div.setAttribute("style","border-bottom-right-radius: 20px; border-top-right-radius: 20px; padding: 5px; padding-right: 10px;")
    cross = document.createElement("h6")
    cross.setAttribute("style","cursor: pointer;")
    cross.innerHTML = "&times;"
    // onclick, remove panel and like
    cross.addEventListener("click", function(){
      fetch(`/like/${like_id}/${group_id}`, {
            method: 'PUT',
            body: JSON.stringify({
                like: false
            })
        }).then(response => {
            fetch(`/like/${like_id}/${group_id}`)
            .then(response => response.json())
            .then(gift => {
                // console.log(gift)
                for(var i = 0; i < like_count.length; i ++){
                  like_count[i].innerHTML = gift.likes
                }
                // console.log(like_count.innerHTML)

            });
        }

        )

    var remove_panel = document.getElementById(`${like_id}-${group_id}-gift-wishlist`)
    remove_panel.remove()

    var like_objects = document.querySelectorAll(`.like-btn-${like_id}-${group_id}`)


        for(var k = 0; k < like_objects.length; k++){
        if( like_objects[k].style.color=="red"){
          like_objects[k].style.color = 'white'
          console.log(like_objects[k])

        }
        
      }
    return false;
    })

    cross_div.appendChild(cross)
    




    panel.appendChild(image_div)
    panel.appendChild(description_div)
    panel.appendChild(cross_div)


    wishlist_div = document.getElementById(`${group_id}-wishlist`)
    wishlist_div.appendChild(panel)


    fetch(`/like/${like_id}/${group_id}`, {
            method: 'PUT',
            body: JSON.stringify({
                like: true
            })
        }).then(response => {
            fetch(`/like/${like_id}/${group_id}`)
            .then(response => response.json())
            .then(gift => {
                console.log(gift)
                for(var i = 0; i < like_count.length; i ++){
                  like_count[i].innerHTML = gift.likes
                }
                // like_count.innerHTML = gift.likes;

                // console.log(like_count.innerHTML)

            });
        }

        )
        // like_object.style.color = 'red'

        var like_objects = document.querySelectorAll(`.like-btn-${like_id}-${group_id}`)


        for(var k = 0; k < like_objects.length; k++){
        if( like_objects[k].style.color=="white"){
          like_objects[k].style.color = 'red'
          console.log(like_objects[k])

        }
        
      }


        return false;



        


  }else{
    
    var count = wishlist_count.getAttribute("value")
    console.log(count)
    count -= 1
    wishlist_count.innerHTML = count
    wishlist_count.setAttribute("value", count)
    
    // need to delete that gift from wishlist

    fetch(`/like/${like_id}/${group_id}`, {
            method: 'PUT',
            body: JSON.stringify({
                like: false
            })
        }).then(response => {
            fetch(`/like/${like_id}/${group_id}`)
            .then(response => response.json())
            .then(gift => {
                // console.log(gift)
                for(var i = 0; i < like_count.length; i ++){
                  like_count[i].innerHTML = gift.likes
                }
                // console.log(like_count.innerHTML)

            });
        }

        )


        // add back after creating it in db

    var remove_panel = document.getElementById(`${like_id}-${group_id}-gift-wishlist`)
    remove_panel.remove()

    var like_objects = document.querySelectorAll(`.like-btn-${like_id}-${group_id}`)


        for(var k = 0; k < like_objects.length; k++){
        if( like_objects[k].style.color=="red"){
          like_objects[k].style.color = 'white'
          console.log(like_objects[k])

        }
        
      }
    return false;
  }

  // console.log(like_id, group_id)

}


