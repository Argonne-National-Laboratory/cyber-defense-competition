window.graphs = new Array();

function teamGraph(team_num) {
  CanvasJS.addColorSet("teamColors", ["#2e8b57", "red", "steelblue"])

  $.getJSON("/data", function(data) {

    points = []
    data.forEach(function(d) {
      if (d.num == team_num) {
        points.push({x: 1, y: parseInt(d.user)},
                    {x: 2, y: parseInt(d.attacker)},
                    {x: 3, y: parseInt(d.defender)})
      }

    });

    var options = {
      colorSet: "teamColors",
      axisX: {
        tickLength: 0,
        lineThickness: 0,
        labelFontSize: 1,

      },
      axisY: {
        maximum: 3100,
        tickLength: 0,
        lineThickness: 0,
        labelFontSize: 1,
      },
      width:200,
      height:50,

      data: [{
        type: "bar",
        dataPoints: points
      }]
    }
    var divid = "g"+team_num;

    window.graphs[team_num] = new CanvasJS.Chart(divid, options);
  });
}

function updateGraph(team_num) {
  try {
  $.getJSON("/data", function(data) {
      points = []
      data.forEach(function(d) {
        if (d.num == team_num) {
          points.push({x: 1, y: parseInt(d.user)},
                      {x: 2, y: parseInt(d.attacker)},
                      {x: 3, y: parseInt(d.defender)})
        }

      });
      divid = "#g"+team_num;
      console.log('team '+team_num);
      window.graphs[team_num].options.data.dataPoints = points;
      window.graphs[team_num].render();
    });
    exploder(team_num, attacker);
  } catch(err) {
    console.log("couldn't read csv");
  }
}

function exploder(team_num, attacker) {
  var divid = "#td"+team_num+" .explode";
  if (parseInt(attacker) > 2500) {
    console.log("exploding team "+team_num+" at "+attacker+" via "+divid);
    $(divid).show();
  } else if (parseInt(attacker) <= 2500) {
    $(divid).hide();
  }
}
