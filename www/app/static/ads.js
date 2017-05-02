(function () {
  $(document).ready(function() {
    $('div.ad').each(function () {
      var a = document.createElement('a');
      var url = $(this).data('host') + '/ads/get?type=' + $(this).data('spot');
      var div = $(this);
      a.href = url;

      // Only served from the https api
      if (!/^https:$/.test(a.protocol) || !/\.blockchain\.info$/.test(a.hostname)) {
        return;
      }

      $.ajax({
        url: url,
        dataType: 'json',
        cors: true,
        success: function(data) {
          a.href = data.url;

          if (!/^https?:$/.test(a.protocol)
              || a.host == ""
              || a.host == window.location.host
              || !/^data:image\/(png|jpg|jpeg|gif);base64,/.test(data.data)
              || !/\.blockchain\.info$/.test(a.hostname)) {
            return;
          }

          var img = $('<img>').attr('src', data.data);
          div.append(img);
          div.wrapInner($('<a></a>').attr('href', data.url));
        }
      });
    });
  });
})();
