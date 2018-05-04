$(function() {
var host = "http://localhost:8000/rhlist";

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

function onRhListRequestShow(need_page_idx_query) {
  var url = host;
  var query = "";
  var hasQuery = false;

  // select area
  privinceSelected = $("#privince").text();
  citySelected = $("#city").text();
  areaSelected = $("#area").text();

  if (privinceSelected.length != 0) {
    if (hasQuery) {
      query = query + "&"
    }
    query = query + "prov=" + privinceSelected;
    hasQuery = true;
  }

  if (citySelected.length != 0) {
    if (hasQuery) {
      query = query + "&"
    }
    query = query + "city=" + citySelected;
    hasQuery = true;
  }

  if (areaSelected.length != 0) {
    if (hasQuery) {
      query = query + "&"
    }
    query = query + "area=" + areaSelected;
    hasQuery = true;
  }

  // select price, bednum, type, property, etc.
  priceSelected = $("#priceList").children(".selected-item").attr("data-index");
  bedSelected = $("#bedList").children(".selected-item").attr("data-index");
  typeSelected = $("#typeList").children(".selected-item").attr("data-index");
  propSelected = $("#propList").children(".selected-item").attr("data-index");
  if (need_page_idx_query) {
      pageSelected = $("#page-idx").children(".selected-page-idx").attr("data-page-index");
  }

  if (priceSelected != "0") {
    if (hasQuery) {
      query = query + "&"
    }
    query = "price=" + priceSelected;
    hasQuery = true;
  }
  if (bedSelected != "0") {
    if (hasQuery) {
      query = query + "&"
    }
    query = query + "bed=" + bedSelected;
    hasQuery = true;
  }
  if (typeSelected != "0") {
    if (hasQuery) {
      query = query + "&"
    }
    query = query + "type=" + typeSelected;
    hasQuery = true;
  }
  if (propSelected != "0") {
    if (hasQuery) {
      query = query + "&"
    }
    query = query + "prop=" + propSelected;
    hasQuery = true;
  }

  if (need_page_idx_query && pageSelected != "1") {
      if (hasQuery) {
          query = query + "&"
      }
      query = query + "page=" + pageSelected;
      hasQuery = true;
  }

  if (query != undefined && query.length > 0) {
    url = url + "?" + query;
  }

  window.location.href = url;
}

$(".selected-item").click(function(e) {
  onRhListRequestShow(false);
}

$(".unselect-item").click(function(e) {
  targetElem = $(e.target);
  var selectedElem = targetElem.siblings(".selected-item")
  if (selectedElem.length != 1 || targetElem.length != 1) {
      console.error("Selector [ .selected-item ] or click target : count != 1");
  }
  selectedElem.removeClass("selected-item");
  selectedElem.addClass("unselect-item");
  targetElem.removeClass("unselect-item");
  targetElem.addClass("selected-item");

  targetElem.parent().parent().collapse('hide');
  //$('#identifier').collapse('hide');

  onRhListRequestShow(false);
});

$(".unselect-page-idx").click(function(e) {
  targetElem = $(e.target);
  var selectedElem = targetElem.siblings(".selected-page-idx")
  if (selectedElem.length != 1 || targetElem.length != 1) {
      console.error("Selector [ .selected-page-idx ] or click target : count != 1");
  }
  selectedElem.removeClass("selected-page-idx");
  selectedElem.addClass("unselect-page-idx");
  targetElem.removeClass("unselect-page-idx");
  targetElem.addClass("selected-page-idx");

  onRhListRequestShow(true);
});

var spyObj = new spyObject($("#rh_list_title_bar"), "stick_fixed", $("#rh_list"));
spyObj.init();







});
