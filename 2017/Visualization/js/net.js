window.lines = []

var colors = new Array();
for(col=0x0;col<=0xFFFFFF;col++) {
  colors.push("#" + col);
}
setTimeout( function() {
    id();
}, 2000);

setInterval(function() {
  updateLinks();
}, 3000);

setInterval(function() {
  updateSmallLinks();
}, 7000);

function id() {
    window.l = new Map();
    $("line").each(function(index) {
        //$(this).css("stroke", colors[index*22]);
        var ourId = "l"+index;
        $(this).attr("id", ourId);
    })
    window.n = new Map()
    $(".node").each(function(index) {
        //$(this).css("fill", colors[index*13]);
        var ourId = "n"+index
        $(this).attr("id", ourId);
    })
 }

function updateLinks() {
  $.getJSON("/data", function(data) {
    data.forEach(function(d) {
      var thresholds = [1000,1500,2000,2500];
      $.getJSON("/lines", function(lines) {
        console.log("l "+lines[d.name]);
        if (d.attacker < thresholds[0]) {
          $("#"+lines[d.name]).css("stroke-width", "1");
        } else if (d.attacker >= thresholds[0] && d.attacker < thresholds[1]) {
          $("#"+lines[d.name]).css("stroke-width", "2");
        } else if (d.attacker >= thresholds[1] && d.attacker < thresholds[2]) {
          $("#"+lines[d.name]).css("stroke-width", "4");
          $("#"+lines[d.name]).css("stroke", "red");
        } else if (d.attacker >= thresholds[2] && d.attacker < thresholds[3]) {
          $("#"+lines[d.name]).css("stroke-width", "5");
          $("#"+lines[d.name]).css("stroke", "red");
        } else if (d.attacker >= thresholds[4]) {
          $("#"+lines[d.name]).css("stroke-width", "8");
          $("#"+lines[d.name]).css("stroke", "red");
        }
      })
    })
  })
}

function updateSmallLinks() {
  var thresholds = [1000,1500,2000,2500];
  $.getJSON("/lines", function(lines) {
    $.getJSON("/data", function(data) {
      data.forEach(function(d) {
        for (var ip in lines) {
          if (d[ip]) {
            console.log("ip: "+ip+" id: "+lines[ip]+" val: "+d[ip]);
            if (d[ip] < thresholds[0]) {
              $("#"+lines[ip]).css("stroke-width", "1");
            } else if (d[ip] >= thresholds[0] && d[ip] < thresholds[1]) {
              $("#"+lines[ip]).css("stroke-width", "2");
            } else if (d[ip] >= thresholds[1] && d[ip]< thresholds[2]) {
              $("#"+lines[ip]).css("stroke-width", "3");
              $("#"+lines[ip]).css("stroke", "red");
            } else if (d[ip] >= thresholds[2] && d[ip] < thresholds[3]) {
              $("#"+lines[ip]).css("stroke-width", "3");
              $("#"+lines[ip]).css("stroke", "red");
            } else if (d[ip] >= thresholds[4]) {
              $("#"+lines[ip]).css("stroke-width", "5");
              $("#"+lines[ip]).css("stroke", "red");
            }
          }
        }
      })
    })
  })
}
