#!/usr/bin/python2
"""HMI for Simmons Systems"""

__author__ = "thompsonm@anl.gov (Mike Thompson)"


import os
import sys
import client
import socket
import easygui
import cherrypy
import webbrowser


try:
  PLC = easygui.enterbox(msg="Enter the ipv4 address of your PLC:")
except:
  PLC = "127.0.0.1"
  
if getattr(sys, 'frozen', False):
  PATH = sys._MEIPASS
else:
  PATH = os.path.abspath(os.path.dirname('__file__'))


SHUTDOWN_PASSWORD = "Set me to something good!"


cherrypy.config.update({'environment': 'embedded',
  'show_tracebacks': True, 'log.screen': True})


class Root(object):
  """Cherrypy class describing our web root."""

  def __init__(self):
    """Default init method"""
    self.saved = {}
    self.client = client

  @cherrypy.expose
  def index(self):
    """Hello world, for index"""
    cherrypy.response.headers["Access-Control-Allow-Origin"] = "*"

    p = """
    <script src="/media/RGraph.common.core.js"></script>
    <script src="/media/RGraph.common.dynamic.js"></script>
    <script src="/media/RGraph.common.effects.js"></script>
    <script src="/media/RGraph.gauge.js"></script>
    <script src="/media/RGraph.vprogress.js"></script>
    <link rel="icon" 
      type="image/png" 
      href="/media/favicon.png">
    <style>
    body {
      background-color: steelblue;
      font-family: 'Roboto', sans;
     }
     .graph {
       margin-top: 20px;
       background-color: rgba(255, 255, 255, 0.4);
       width: 700px;
       box-shadow: 0 1px 7px rgba(0,0,0,0.4);
	   -webkit-border-radius: 4px;
      }
      #loading {
        position: absolute;
        top: 600px;
        right: 0px;
        left: 0px;
        
        }
     .graph {
         stroke-width: 1.5;
      }
        .graph .axis {
            stroke-width: 1;
        }

        .graph .axis .tick line {
            stroke: black;
        }

        .graph .axis .tick text {
            fill: black;
            font-size: 0.7em;
        }

        .graph .axis .domain {
            fill: none;
            stroke: black;
        }

        .graph .group {
            fill: none;
            stroke: black;
            stroke-width: 1.5;
        }
    </style>
    <center><img src="media/Simmons.png" /></br>
    <canvas id="f" width="250" height="250">
    [No canvas support]
    </canvas>
    <canvas id="c" width="250" height="250">
    [No canvas support]
    </canvas>
    <canvas id="v" width="250" height="250">
    [No canvas support]
    </canvas>
    </center>
    <script>
    window.frequency = [];
    window.voltage = [];
    window.current = [];
    function f() {
      var fgauge = new RGraph.Gauge({
        id: 'f',
        min:0,
        max: 90,
        value: 7,
        options: {
          borderOutline: 'transparent',
          needleColors: ['green'],
          needleType: 'line',
          centerpinRadius: 0.1,
          titleTop: 'Frequency (in Hz)',
          labelsOffset: 7
        }
      }).on('draw', function (obj) {
        var fco = obj.context;

        // This circle becomes the border of the centerpin
        RGraph.path(fco, ['b', 'a', obj.centerx, obj.centery, 10, 0, RGraph.TWOPI, false, 'f', 'black']);
      })
      .draw();
      var delay = 500;
      function fmyAJAXCallback(num) {
        window.frequency.push(parseInt(num));
        fgauge.value = num;
        fgauge.grow()    
            
        // Make another AJAX call after the delay (which is in milliseconds)
        setTimeout(function () {
          RGraph.AJAX.getNumber('/get_f', fmyAJAXCallback);
        }, delay);
      }
          /**
     * Make the AJAX call every so often (contolled by the delay variable)
     */
    setTimeout(function () {

      RGraph.AJAX.getNumber('/get_f', fmyAJAXCallback);
    }, delay);
    };
       function c() {
      var cgauge = new RGraph.Gauge({
        id: 'c',
        min:0,
        max: 200,
        value: 7,
        options: {
          borderOutline: 'transparent',
          needleColors: ['orange'],
          needleType: 'line',
          centerpinRadius: 0.1,
          titleTop: 'Current (in Amps)',
          labelsOffset: 7
        }
      }).on('draw', function (obj) {
        var cco = obj.context;

        // This circle becomes the border of the centerpin
        RGraph.path(cco, ['b', 'a', obj.centerx, obj.centery, 10, 0, RGraph.TWOPI, false, 'f', 'black']);
      })
      .draw();
      var delay = 500;
      function cmyAJAXCallback(num) {
        window.current.push(parseInt(num));
        cgauge.value = num;
        cgauge.grow()    
            
        // Make another AJAX call after the delay (which is in milliseconds)
        setTimeout(function () {
          RGraph.AJAX.getNumber('/get_c', cmyAJAXCallback);
        }, delay);
      }
          /**
     * Make the AJAX call every so often (contolled by the delay variable)
     */
    setTimeout(function () {

      RGraph.AJAX.getNumber('/get_c', cmyAJAXCallback);
    }, delay);
    };
       function v() {
      var vgauge = new RGraph.Gauge({
        id: 'v',
        min:0,
        max: 550,
        value: 7,
        options: {
          borderOutline: 'transparent',
          needleColors: ['grey'],
          needleType: 'line',
          centerpinRadius: 0.1,
          titleTop: 'Voltage (in Volts)',
          labelsOffset: 7
        }
      }).on('draw', function (obj) {
        var vco = obj.context;

        // This circle becomes the border of the centerpin
        RGraph.path(vco, ['b', 'a', obj.centerx, obj.centery, 10, 0, RGraph.TWOPI, false, 'f', 'black']);
      })
      .draw();
      var delay = 500;
      function vmyAJAXCallback(num) {
        window.voltage.push(parseInt(num));
        vgauge.value = num;
        vgauge.grow()    
            
        // Make another AJAX call after the delay (which is in milliseconds)
        setTimeout(function () {
          RGraph.AJAX.getNumber('/get_v', vmyAJAXCallback);
        }, delay);
      }
          /**
     * Make the AJAX call every so often (contolled by the delay variable)
     */
    setTimeout(function () {

      RGraph.AJAX.getNumber('/get_v', vmyAJAXCallback);
    }, delay);
    };
    f();
    c();
    v();
    function shutdownSystem() {
      RGraph.AJAX.POST("/shutdown")
    }
</script><br /><center>
    <button onclick=shutdownSystem()>Emergency 
    Shutdown</button></center>
    <centeR><div class="graph"></div>
        <script src="http://d3js.org/d3.v3.min.js"></script>
        <script>
        var limit = 60 * 1,
            duration = 750,
            now = new Date(Date.now() - duration)

        var width = 700,
            height = 350

        var groups = {
            current: {
                value: 0,
                color: 'orange',
                data: d3.range(limit).map(function() {
                    return 0
                })
            },
            target: {
                value: 0,
                color: 'green',
                data: d3.range(limit).map(function() {
                    return 0
                })
            },
            output: {
                value: 0,
                color: 'grey',
                data: d3.range(limit).map(function() {
                    return 0
                })
            }
        }

        var x = d3.time.scale()
            .domain([now - (limit - 2), now - duration])
            .range([0, width])

        var y = d3.scale.linear()
            .domain([0, 300])
            .range([height, 0])

        var line = d3.svg.line()
            .interpolate('basis')
            .x(function(d, i) {
                return x(now - (limit - 1 - i) * duration)
            })
            .y(function(d) {
                return y(d)
            })

        var svg = d3.select('.graph').append('svg')
            .attr('class', 'chart')
            .attr('width', width)
            .attr('height', height + 50)

        var axis = svg.append('g')
            .attr('class', 'x axis')
            .attr('transform', 'translate(0,' + height + ')')
            .call(x.axis = d3.svg.axis().scale(x).orient('bottom'))

        var paths = svg.append('g')

        for (var name in groups) {
            var group = groups[name]
            console.log("data "+group.data);
            group.path = paths.append('path')
                .data([group.data])
                .attr('class', name + ' group')
                .style('stroke', group.color)
        }

        function tick() {
        now = new Date()

            // Add new values
            for (var name in groups) {
                var group = groups[name]
                //group.data.push(group.value) // Real values arrive at irregular intervals
                if (name == "current") {
                  data = window.current.pop()
                } else if (name == "target") {
                  data = window.frequency.pop()
                } else if (name == "output") {
                  data = window.voltage.pop()
                }
                group.data.push(data)
                group.path.attr('d', line)
                console.log("name: "+name+" data: "+data+" line: "+line)
            }

            // Shift domain
            x.domain([now - (limit - 2) * duration, now - duration])

            // Slide x-axis left
            axis.transition()
                .duration(duration)
                .ease('linear')
                .call(x.axis)

            // Slide paths left
            paths.attr('transform', null)
                .transition()
                .duration(duration)
                .ease('linear')
                .attr('transform', 'translate(' + x(now - (limit - 1) * duration) + ')')
                .each('end', tick)

            // Remove oldest data point from each group
            for (var name in groups) {
                var group = groups[name]
                group.data.shift()
            }
        }

        tick()
        </script>
        <div id="loading"><img src=media/76.gif /><br />Loading...</div>
        <script>
        setTimeout(function() {
          d3.select("#loading").style("display", "none");
        }, 40000);
        </script>
    """ 
    return p
    
  @cherrypy.expose
  def get_f(self):
    try:
      return "%d" % client.get_val(PLC, 8)
    except:
      return "0"
	  	
  @cherrypy.expose  
  def get_c(self):
    try:
      return "%d" % client.get_val(PLC, 16)	
    except:
      return "0"

  @cherrypy.expose
  def get_v(self):
    try:
      return "%d" % client.get_val(PLC, 24)
    except:
      return "0"

    
  @cherrypy.expose
  def shutdown(self):
    server_address = (PLC, 20001)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(server_address)
    sock.sendall(SHUTDOWN_PASSWORD)

  @cherrypy.expose
  def plot(self):
    fig = plt.figure()
    ax = plt.axes(xlim=(0, 100), ylim=(0, 1023))
    a0, = ax.plot([], [])
    a1, = ax.plot([], [])
    anim = animation.FuncAnimation(fig, self. client.get_val, 
                                 fargs=(PLC, 24), 
                                 interval=50)
    # show plot
    plt.show()


static_config={
  '/media': {
    'tools.staticdir.on': True,
    'tools.staticdir.dir': os.path.join(PATH, "media"),

    'log.screen': True,
  },
  '/favicon.ico': {
    'tools.staticfile.on': True,
    'tools.staticfile.filename': os.path.join(PATH, "favicon.ico")
  }
}

	  
cherrypy.config.update({'server.socket_host': '0.0.0.0',
                         'server.socket_port': 1337,
                        })
cherrypy.tree.mount(Root(), '/', static_config)
cherrypy.server.socket_port = 1337
cherrypy.config.update(static_config)
cherrypy.engine.start()
webbrowser.open("http://127.0.0.1:1337/")
cherrypy.engine.block()

