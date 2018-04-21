function spyObject(spyElement, stickClass, brother, stickFunc) {
  var spyOffset = function() {
    if ($(spyElement).length != 1) {
      console.error("Selector [" + spyElement + "] count != 1");
      return;
    }
    var h = $(spyElement).outerHeight();
    // var s = $('<div class="occupy" style="display: none; height: '+ offset.height +'px">');
    var s = $('<div class="occupy" style="display: none; height: '+ h +'px">');
    var inserted = false;
    if (!inserted) {
      if ($(spyElement).next().length != 0) {
        s.insertBefore($(spyElement).next());
      } else {
        s.appendTo($(spyElement).parent());
      }
      inserted = true;
    }
    var onViewScroll = function() {
      var offset = $(spyElement).offset()
      var offsetWindow = (document.body.scrollTop || document.documentElement.scrollTop);
      var h = $(spyElement).outerHeight();
      var offset0 = $(brother).offset();
      if (offset0.top - h < offsetWindow) {
        $(spyElement).addClass(stickClass);
        $(".occupy").css("display","block");
        // if (stickFunc != None)
      } else {
        $(spyElement).removeClass(stickClass);
        $(".occupy").css("display","none");
        // if (stickFunc != None)
      }
    }
    $(window).scroll(onViewScroll);
    $("body").on("touchmove", onViewScroll);
    // offset 
  }
  return {
    init: spyOffset,
    reset: function() {
      $(spyElement).removeClass(stickClass);
      $(".occupy").css("display","none");
    },
    destroy: function() {
      $(window).off("scroll", onViewScroll);
    },
  }
}

