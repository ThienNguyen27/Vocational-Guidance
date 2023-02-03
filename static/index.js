function deleteNote(noteId) {
    fetch("/delete-note", {
      method: "POST",
      body: JSON.stringify({ noteId: noteId }),
    }).then((_res) => {
      window.location.href = "/";
    });
  }
  
function closeButton(){ 
    document.getElementById('flash_noti').setAttribute("style", "display:none");
} 