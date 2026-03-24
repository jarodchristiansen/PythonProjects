const theContent = $('#content2');

$('#save').on('click', function(){
  const editedContent = theContent.html();
  localStorage.newContent = editedContent;
});


if(localStorage.getItem('newContent')) {
  theContent.html(localStorage.getItem('newContent'));
}