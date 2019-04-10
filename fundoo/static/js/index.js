//$(document).ready(function(){
//$("#menu-toggle").click(function(e) {
//// e.preventDefault();
////
////console.log(e);
//$("#wrapper").toggleClass("active");
////$( ".panel-danger " ).css('margin-left','22%');
//// $( "#column" ).css('margin-left','20%');
///* alert(1);*/
//});


});



  <script src="https://code.jquery.com/jquery-2.2.4.min.js" type="text/javascript"></script>

  <script>
      function changeColor(element,id) {
            var color=element.name
            var id=id
            console.log(color)
            console.log(id)
            $.ajax({
              method: 'POST',
              url: '/setcolor/',
              data: {
                'color': color,
                'id':id,
                'csrfmiddlewaretoken': window.CSRF_TOKEN // from index.html
              },
              success: function(data) {
                location.reload();
                console.log(data)
               <!--document.getElementById("note-card").style.backgroundColor = color-->
              },
              error: function(xhr, status, error) {
                // shit happens friends!
              }
            });
        }
        function pinned(element,id) {
            var id=id
            console.log(id)
            $.ajax({
              method: 'POST',
              url: '/ispinned/',
              data: {
                'id':id,
                'csrfmiddlewaretoken': window.CSRF_TOKEN // from index.html
              },
          success: function(data) {
           console.log(data)
           location.reload();
          },
          error: function(xhr, status, error) {
            // shit happens friends!
          }
        });
        }
         function archived(element,id) {
            var id=id
            console.log(id)
            $.ajax({
            method: 'POST',
            url: '/isarchive/',
            data: {
            'id':id,
            'csrfmiddlewaretoken': window.CSRF_TOKEN // from index.html
            },
            success: function(data) {
            console.log(data)
             location.reload();
            },
            error: function(xhr, status, error) {
            // shit happens friends!
            }
            });
         }
  </script>